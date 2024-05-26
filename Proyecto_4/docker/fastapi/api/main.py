from fastapi import FastAPI, HTTPException
from api.schemas import HouseData
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
model_prod_uri = "models:/{model_name}/production".format(model_name=model_name)
model = mlflow.pyfunc.load_model(model_uri=model_prod_uri)


# Initialize FastAPI
app = FastAPI()


# Define endpoint for root URL
@app.get("/")
async def root():
    return {"message": "Welcome to the Hose Price Prediction API!"}


# Define endpoint for prediction
@app.post("/predict")
async def predict_price(data: HouseData):
    # Perform prediction
    prediction = model.predict(
        [
            {
                'status': data.status,
                'bed': data.bed,
                'bath': data.bath,
                'acre_lot': data.acre_lot,
                'state': data.state,
                'house_size': data.house_size,
            }
        ]
    )
    # Convertir el resultado de la predicción a un diccionario
    prediction_dict = {
        "prediction": str(prediction[0])
    }  # Convertir la predicción a una cadena
    
    # Crear un diccionario con los datos
    datos = {
        'status': [data.status],
        'bed': [data.bed],
        'bath': [data.bath],
        'acre_lot': [data.acre_lot],
        'state': [data.state],
        'house_size': [data.house_size],
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