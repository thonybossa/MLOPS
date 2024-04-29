from fastapi import FastAPI, HTTPException
from typing import Optional
import random
import json
import time
import csv
import os

MIN_UPDATE_TIME = 5
GROUP_NUMBER = "3" 

app = FastAPI()

@app.get("/")
async def root():
    return {"Proyecto 3": "Extracción de Base de Datos de Diabetes"}

data = []
with open("Diabetes/df_train_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        data.append(row)

test_data = []
with open("Diabetes/df_test_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        test_data.append(row)

validation_data = []
with open("Diabetes/df_validation_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        validation_data.append(row)



batch_size = len(data) // 6


# Definir la función para generar la fracción de datos aleatoria
def get_batch_data(batch_number: int, batch_size: int = batch_size):
    start_index = batch_number * batch_size
    end_index = start_index + batch_size
    # Obtener datos aleatorios dentro del rango del grupo
    random_data = random.sample(data[start_index:end_index], batch_size)
    return random_data

if os.path.isdir(f"/Diabetes/timestamp") == False:
    os.mkdir(f"/Diabetes/timestamp")


if os.path.isfile("/Diabetes/timestamp/timestamps.json"):
    with open("/Diabetes/timestamp/timestamps.json", "r") as f:
        timestamps = json.load(f)
else:
    timestamps = {GROUP_NUMBER: [0, -1]}

# Definir la ruta de la API
@app.get("/data_train")
async def read_data():
    global timestamps

    if timestamps[GROUP_NUMBER][1] >= 6:
        raise HTTPException(status_code=400,detail="Ya se recolectó toda la información minima necesaria")

    current_time = time.time()
    last_update_time = timestamps[GROUP_NUMBER][0]

    if current_time - last_update_time > MIN_UPDATE_TIME:
        timestamps[GROUP_NUMBER][0] = current_time
        timestamps[GROUP_NUMBER][1] += 1

    random_data = get_batch_data(timestamps[GROUP_NUMBER][1])
    with open("/Diabetes/timestamp/timestamps.json", "w") as file:
        file.write(json.dumps(timestamps))

    return {"group_number": GROUP_NUMBER, "batch_number": timestamps[GROUP_NUMBER][1] + 1,"data": random_data}


# Get data in batches
@app.get("/data_validation")
async def read_data_validation():
    return {"data": validation_data}


# Get data in batches
@app.get("/data_test")
async def read_data_test():
    return {"data": test_data}


@app.get("/restart_data_generation")
async def restart_data():
    timestamps[GROUP_NUMBER][0] = 0
    timestamps[GROUP_NUMBER][1] = -1
    with open("/Diabetes/timestamp/timestamps.json", "w") as file:
        file.write(json.dumps(timestamps))

    return {"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8086)