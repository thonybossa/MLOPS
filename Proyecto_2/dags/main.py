from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from airflow.decorators import dag , task 
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import pickle
import requests
from sqlalchemy import create_engine , inspect
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
import time
restart_api = 0
log = 0

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(start_date=datetime(2024, 3, 9), schedule_interval='@daily', catchup=False)
def pipeline():

    
    @task
    def load_data(index= int):
        if index > 0:  # No esperar antes de la primera ejecución
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
        feature_names = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
       'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
       'Horizontal_Distance_To_Fire_Points', 'Wilderness_Area', 'Soil_Type',
       'Cover_Type']
        cat_features_indices = [df_final.columns.get_loc(name) for name in feature_names]  # Obtiene los índices de las columnas categóricas


        # Dividir los datos en características (X) y variable objetivo (y)
        X = df_final.drop('Cover_Type', axis=1)
        y = df_final['Cover_Type']

        # Realizar la partición de los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Crear una instancia del modelo CatBoostClassifier
        model = CatBoostClassifier()

        # Entrenar el modelo
        model.fit(X_train, y_train , cat_features=cat_features_indices )

        # Guardar el modelo
        with open('model_catboost.pkl', 'wb') as f:
            pickle.dump(model, f)

    start = DummyOperator(task_id='start')
    prev_task = start

    for i in range(10):
        load_task = load_data(i)
        # Con time.sleep ya incluido en load_data, ya no necesitas TimeDeltaSensor
        prev_task = prev_task >> load_task

    train_task = train()
    prev_task >> train_task

    

dag_instance = pipeline()
