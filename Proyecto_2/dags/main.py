
import os
import mlflow
import requests
import numpy as np
import pandas as pd

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
from catboost import CatBoostClassifier
import pickle
from sqlalchemy import create_engine , inspect
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
import time

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Config
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio:9000"
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'

mlflow.set_tracking_uri("http://mlflow:8083")
mlflow.set_experiment('covertype')

@dag(start_date=datetime(2024, 3, 9), schedule_interval='@daily', catchup=False)
def pipeline():

    
    @task
    def load_data(index= int):
        if index > 0:  
            time.sleep(300)

        if index == 0 :
            url = "http://10.43.101.149/restart_data_generation?group_number=3"  
            response = requests.get(url)
            
        response = requests.get("http://10.43.101.149/data?group_number=3")
        data = response.json()

        df = pd.DataFrame(
            columns = [
                "Elevation",
                "Aspect",
                "Slope",
                "Horizontal_Distance_To_Hydrology",
                "Vertical_Distance_To_Hydrology",
                "Horizontal_Distance_To_Roadways",
                "Hillshade_9am",
                "Hillshade_Noon",
                "Hillshade_3pm",
                "Horizontal_Distance_To_Fire_Points",
                "Wilderness_Area",
                "Soil_Type",
                "Cover_Type"
                ]  
            )
        for i in range(len(data['data'])):
            df.loc[i] = data['data'][i]
        
        df['batch'] = data['batch_number']
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        inspector = inspect(engine)
        if inspector.has_table('covered_type'):
            df.to_sql('covered_type', engine, if_exists='append', index=False)
        else:
            df.to_sql('covered_type', engine, if_exists='fail', index=False)
       
    @task
    def train():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')

        df_final = pd.read_sql_table('covered_type', con=engine)
        df_final = df_final.dropna()
        df_final.drop(columns=['batch'], inplace=True)
        feature_names = ['Wilderness_Area', 'Soil_Type']
        cat_features_indices = [df_final.columns.get_loc(name) for name in feature_names]  # Obtiene los índices de las columnas categóricas

        # Dividir los datos en características (X) y variable objetivo (y)
        X = df_final.drop('Cover_Type', axis=1)
        y = df_final['Cover_Type']
        
        # Realizar la partición de los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Crear una instancia del modelo CatBoostClassifier
        model = CatBoostClassifier()

        mlflow.sklearn.autolog(log_model_signatures=True, log_input_examples=True, registered_model_name="best_model")
        with mlflow.start_run(run_name="autolog_pipe_model_reg"):
            model.fit(X_train, y_train, cat_features=cat_features_indices)

    start = DummyOperator(task_id='start')
    prev_task = start

    for i in range(1): # aca se cambia el parametro para el numero de batch
        load_task = load_data(i)
        prev_task = prev_task >> load_task

    train_task = train()
    prev_task >> train_task

    

dag_instance = pipeline()
