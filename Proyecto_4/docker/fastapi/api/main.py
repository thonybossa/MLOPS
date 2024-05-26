from fastapi import FastAPI, HTTPException
from api.schemas import PatientData
from sqlalchemy import create_engine, inspect
import pandas as pd
import os
import mlflow

# Load model
#os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://10.43.101.152:8088"
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio:9000"
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'

#mlflow.set_tracking_uri("http://10.43.101.152:8083")
mlflow.set_tracking_uri("http://mlflow:8083")

model_name = "best_model"
model_version = 1
model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")


# Initialize FastAPI
app = FastAPI()


# Define endpoint for root URL
@app.get("/")
async def root():
    return {"message": "Welcome to the Readmitted Prediction API!"}


# Define endpoint for prediction
@app.post("/predict")
async def predict_readmitted(data: PatientData):
    # Perform prediction
    prediction = model.predict(
        [
            {
                'race': data.race,
                'gender': data.gender,
                'age': data.age,
                'admission_type_id': data.admission_type_id,
                'discharge_disposition_id': data.discharge_disposition_id,
                'admission_source_id': data.admission_source_id,
                'time_in_hospital': data.time_in_hospital,
                'medical_specialty': data.medical_specialty,
                'num_lab_procedures': data.num_lab_procedures,
                'num_procedures': data.num_procedures,
                'num_medications': data.num_medications,
                'number_emergency': data.number_emergency,
                'number_inpatient': data.number_inpatient,
                'diag_1': data.diag_1,
                'diag_2': data.diag_2,
                'diag_3': data.diag_3,
                'number_diagnoses': data.number_diagnoses,
                'insulin': data.insulin,
                'change': data.change,
                'diabetesMed': data.diabetesMed,
            }
        ]
    )
    # Convertir el resultado de la predicción a un diccionario
    prediction_dict = {
        "prediction": str(prediction[0])
    }  # Convertir la predicción a una cadena
    
    # Crear un diccionario con los datos
    datos = {
        'race': [data.race],
        'gender': [data.gender],
        'age': [data.age],
        'admission_type_id': [data.admission_type_id],
        'discharge_disposition_id': [data.discharge_disposition_id],
        'admission_source_id': [data.admission_source_id],
        'time_in_hospital': [data.time_in_hospital],
        'medical_specialty': [data.medical_specialty],
        'num_lab_procedures': [data.num_lab_procedures],
        'num_procedures': [data.num_procedures],
        'num_medications': [data.num_medications],
        'number_emergency': [data.number_emergency],
        'number_inpatient': [data.number_inpatient],
        'diag_1': [data.diag_1],
        'diag_2': [data.diag_2],
        'diag_3': [data.diag_3],
        'number_diagnoses': [data.number_diagnoses],
        'insulin': [data.insulin],
        'change': [data.change],
        'diabetesMed': [data.diabetesMed],
        'prediction': prediction[0]
    }

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame(datos)
    engine = create_engine('mysql+mysqlconnector://ab:ab@mysql/Base_de_Datos')
    inspector = inspect(engine)
    if inspector.has_table('fastapi_predictions'):
        df.to_sql('fastapi_predictions', engine, if_exists='append', index=False)
    else:
        df.to_sql('fastapi_predictions', engine, if_exists='fail', index=False)
    
    return prediction_dict
