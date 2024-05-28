import os
import mlflow
import requests
import numpy as np
import pandas as pd
import time
import pickle

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from airflow.decorators import dag , task 
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine , inspect
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.operators.dummy import DummyOperator
from sklearn.metrics import confusion_matrix
from airflow.models import Variable
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from airflow.operators.python import PythonOperator, BranchPythonOperator

# Config
#os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://10.43.101.152:8088"
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio:9000"
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'

mlflow.set_tracking_uri("http://mlflow:8083")
mlflow.set_experiment('House Price')
mlflow.sklearn.autolog(log_model_signatures=True, log_input_examples=True, registered_model_name="best_model")

@dag(start_date=datetime(2024, 3, 9), schedule_interval='@daily', catchup=False)
def pipeline():

    @task
    def load_historical_data():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        df = pd.read_sql('SELECT * FROM clean_data_price', engine)
        return df
    
    @task
    def perform_pca_and_compare(historical_data, new_data):
        categorical_features = historical_data.select_dtypes(include=['object']).columns.tolist()
        column_transformer = ColumnTransformer(
            [("encoder", OneHotEncoder(handle_unknown='ignore'), categorical_features)],
            remainder='passthrough'
        )

            # PCA Pipeline
        pca_pipeline = Pipeline([
            ("transform", column_transformer),
            ("scaler", StandardScaler(with_mean=False)),
            ("SVD", TruncatedSVD(n_components=2))
        ])

            # Process both datasets
        historical_processed = pca_pipeline.fit_transform(historical_data)
        new_processed = pca_pipeline.transform(new_data)

            # Compute distances between the principal components of each dataset
        distance = np.linalg.norm(np.mean(historical_processed, axis=0) - np.mean(new_processed, axis=0))
        return distance > 0.1  
    
    @task
    def decision_task(ti):
        pca_result = ti.xcom_pull(task_ids='perform_pca_and_compare', key='pca_result')
        return 'clean_data' if pca_result else 'skip_training'

    
    @task
    def load_data(index= int):
        if index > 0:  
            time.sleep(6)

        if index == 0 :
            url = "http://10.43.101.149/restart_data_generation?group_number=3"  
            #url = "http://host.docker.internal:8084/restart_data_generation"
            response = requests.get(url)
            
        response = requests.get("http://10.43.101.149/data?group_number=3")
        #response = requests.get("http://host.docker.internal:8084/data_train")
        data = response.json()

        df = pd.DataFrame(
            [
                'brokered_by',
                'status',
                'price',
                'bed',
                'bath',
                'acre_lot',
                'street',
                'city',
                'state',
                'zip_code',
                'house_size',
                'pre_sold_state'
            ]
        )
        
        df = pd.DataFrame.from_dict(data['data']).reset_index(drop=True)
        df['batch'] = data['batch_number']
        
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        inspector = inspect(engine)

        if inspector.has_table('raw_data_price'):
            df.to_sql('raw_data_price', engine, if_exists='append', index=False)
        else:
            df.to_sql('raw_data_price', engine, if_exists='fail', index=False)
        return df

    @task
    def clean_data():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos', pool_pre_ping=True)
        df = pd.read_sql('SELECT * FROM raw_data_price', engine)

        df = df.dropna()
        df.replace("", np.nan, inplace=True)
        df.replace("?", np.nan, inplace=True)

        # Lista de columnas a eliminar
        columns_to_drop = [
            'batch',
            'brokered_by',
            'prev_sold_date',
            'zip_code',
            'street',
            'city'
        ]

        # Eliminar las columnas especificadas
        df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

        df_cleaned.to_sql('clean_data_price', engine, if_exists='replace', index=False, chunksize=1000)

       
    @task
    def train():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        df = pd.read_sql('SELECT * FROM clean_data_price', engine)

        # Preparar datos
        X = df.drop(columns=['price'])
        y = df['price']

        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        # Preparar el ColumnTransformer
        column_trans = make_column_transformer(
            (OneHotEncoder(handle_unknown='ignore'), categorical_features),
            remainder='passthrough')
        
        # Crear el pipeline
        pipe = Pipeline(
            steps = 
            [
                ("column_trans", column_trans),
                ("scaler", StandardScaler(with_mean=False)),
                ("classifier", RandomForestRegressor())
            ]
        )
 
        # Parámetros para GridSearchCV
        param_grid = {
            'classifier__max_depth': [1, 2, 3, 10],
            'classifier__n_estimators': [10, 11]
        }
 
        # Preparar GridSearchCV
        search = GridSearchCV(pipe, param_grid, n_jobs=2)
 
        # Dividir los datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
 
        # Iniciar un experimento de MLflow y ajustar el modelo
        #mlflow.end_run()
        with mlflow.start_run(run_name="autolog_with_pipeline") as run:
            search.fit(X_train, y_train)
            print("Mejores parámetros:", search.best_params_)
            print("Mejor puntuación:", search.best_score_)
    @task
    def skip_training():
        print("NO se entrena el modelo")


    start = DummyOperator(task_id='start')
    load_historical = load_historical_data()
    for i in range(1): # se cambia el parametro para el numero de batch
        load_new = load_data(i)
        pca_result = perform_pca_and_compare(load_historical, load_new)
        decision_task = BranchPythonOperator(
            task_id='decision_task',
            python_callable=lambda pca_result: 'clean_data' if pca_result else 'skip_training',
            provide_context=True,
            op_args=[pca_result],
        )   
        

        clean = clean_data()
        train = train()
        skip_training = DummyOperator(task_id='skip_training')

        load_historical >> load_new >> pca_result >> decision_task
        decision_task >> clean >> train
        decision_task >> skip_training

dag_instance = pipeline()