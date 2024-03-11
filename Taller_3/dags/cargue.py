from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from airflow.decorators import dag , task 


@dag(start_date=datetime(2024, 3, 9), schedule_interval='@daily', catchup=False)
def load_penguin_data():

    @task
    def load_data():
        df = pd.read_csv('/opt/airflow/path/penguins_lter.csv')
        engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')
        df.to_sql('penguin_data', engine, if_exists='replace', index=False)
    @task
    def clean_db():
        engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')
        with engine.begin() as connection:
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN "studyName";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Sample Number";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Region";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Stage";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Individual ID";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Clutch Completion";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Date Egg";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Delta 15 N (o/oo)";') 
            connection.execute('ALTER TABLE public.penguin_data DROP COLUMN  "Delta 13 C (o/oo)";') 
               
    load_data() >> clean_db() 

dag_instance = load_penguin_data()
