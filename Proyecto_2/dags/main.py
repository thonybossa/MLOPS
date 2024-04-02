from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from airflow.decorators import dag , task 
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import pickle

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

        # Crear una instancia del modelo CatBoostClassifier
        model = CatBoostClassifier(cat_features=cat_features_indices)

        # Entrenar el modelo
        model.fit(X_train, y_train)

        #GUARDAMOS EL MODELO
        with open('model_catboost.pkl', 'wb') as f:

            pickle.dump(model, f)
               
    load_data() >> clean_db() >> train()

dag_instance = pipeline()
