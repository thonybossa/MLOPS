from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from airflow.decorators import dag , task 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier
import pickle
import mlflow
import os

os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://10.43.101.152:8089'  # Cambia esto a la URL de tu servidor MinIO
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'  # Cambia esto a tu clave de acceso de MinIO
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'  # Cambia esto a tu clave secreta de MinIO
mlflow.set_tracking_uri("http://10.43.101.152:8083")

@dag(start_date=datetime(2024, 3, 9), schedule_interval='@daily', catchup=False)
def pipeline():

    @task
    def load_data():
        df = pd.read_csv('/opt/airflow/path/penguins_lter.csv')
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        df.to_sql('penguin_data', engine, if_exists='replace', index=False)
        
    @task
    def clean_db():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
        with engine.begin() as connection:
            connection.execute('ALTER TABLE penguin_data DROP COLUMN `studyName`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Sample Number`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Region`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Stage`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Individual ID`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Clutch Completion`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Date Egg`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Delta 15 N (o/oo)`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Delta 13 C (o/oo)`;') 
            connection.execute('ALTER TABLE penguin_data DROP COLUMN  `Comments`;')
            
    @task
    def train():
        engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')

        df_final = pd.read_sql_table('penguin_data', con=engine)
        df_final = df_final.dropna()

        # Dividir los datos en características (X) y variable objetivo (y)
        X = df_final.drop('Species', axis=1)
        y = df_final['Species']

        # Obtener los índices de las columnas categóricas
        cat_features_indices = [i for i, col in enumerate(X.columns) if X[col].dtype == 'object' or X[col].dtype.name == 'category']

        # Realizar la partición de los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Inicia un experimento MLflow
        with mlflow.start_run():
        
            # Crear una instancia del modelo CatBoostClassifier
            model = CatBoostClassifier(cat_features=cat_features_indices)

            # Entrenar el modelo
            model.fit(X_train, y_train)
            
            # Registra los parámetros del modelo
            mlflow.log_param("coef", model.coef_)
            mlflow.log_param("intercept", model.intercept_)
            
            # Realiza predicciones y calcula el error cuadrático medio
            y_pred = model.predict(X_test)

            # Calcula la precisión
            accuracy = accuracy_score(y_test, y_pred)

            # Registra la métrica del modelo
            mlflow.log_metric("accuracy", accuracy)

            # Guarda el modelo en el registro de MLflow
            mlflow.sklearn.log_model(model, "model")
               
    load_data() >> clean_db() >> train()

dag_instance = pipeline()
