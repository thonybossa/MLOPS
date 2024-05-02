from fastapi import FastAPI, HTTPException
from api.schemas import CoverType
import pandas as pd
import os
import mlflow

# Load model
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio:9000"
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'
mlflow.set_tracking_uri("http://mlflow:8083")


model_name = "best_model"
model_version = 1
model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")


# Initialize FastAPI
app = FastAPI()


# Define endpoint for root URL
@app.get("/")
async def root():
    return {"message": "Welcome to the CoverType Prediction API!"}


# Define endpoint for prediction
@app.post("/predict")
async def predict_cover_type(data: CoverType):
    # Perform prediction
    prediction = model.predict(
        [
            [
                data.race,
                data.gender,
                data.age,
                data.admission_type_id,
                data.discharge_disposition_id,
                data.admission_source_id,
                data.time_in_hospital,
                data.medical_specialty,
                data.num_lab_procedures,
                data.num_procedures,
                data.num_medications,
                data.number_emergency,
                data.number_inpatient,
                data.diag_1,
                data.diag_2,
                data.diag_3,
                data.number_diagnoses,
                data.insulin,
                data.change,
                data.diabetesMed,
            ]
        ]
    )
    # Convertir el resultado de la predicción a un diccionario
    prediction_dict = {
        "prediction": str(prediction[0])
    }  # Convertir la predicción a una cadena
    return prediction_dict
