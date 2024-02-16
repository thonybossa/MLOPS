from fastapi import FastAPI, HTTPException
from api.schemas import PenguinData
import pickle

# Load the trained model
with open("Model/model_catboost.pkl", "rb") as f:
    model = pickle.load(f)

# Initialize FastAPI
app = FastAPI()


# Define endpoint for root URL
@app.get("/")
async def root():
    return {"message": "Welcome to the Penguin Species Prediction API!"}


# Define endpoint for prediction
@app.post("/predict")
async def predict_species(data: PenguinData):
    # Perform prediction
    prediction = model.predict(
        [
            [
                data.Island,
                data.Culmen_Length_mm,
                data.Culmen_Depth_mm,
                data.Flipper_Length_mm,
                data.Body_Mass_g,
                data.Sex,
            ]
        ]
    )
    # Convertir el resultado de la predicción a un diccionario
    prediction_dict = {
        "prediction": str(prediction[0])
    }  # Convertir la predicción a una cadena
    return prediction_dict
