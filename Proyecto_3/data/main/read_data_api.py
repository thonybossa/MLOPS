from fastapi import FastAPI, HTTPException
import random
import json
import time
import csv
import os

MIN_UPDATE_TIME = 5
app = FastAPI()

@app.get("/")
async def root():
    return {"Proyecto": "Extracción de Base de Datos de Diabetes"}

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

batch_size = len(data) // 90

def get_batch_data(batch_number: int, batch_size: int = batch_size):
    start_index = batch_number * batch_size
    end_index = start_index + batch_size
    random_data = random.sample(data[start_index:end_index], batch_size)
    return random_data

if not os.path.isdir("Diabetes/timestamp"):
    os.mkdir("Diabetes/timestamp")

if os.path.isfile("Diabetes/timestamp/timestamps.json"):
    with open("Diabetes/timestamp/timestamps.json", "r") as f:
        timestamps = json.load(f)
else:
    timestamps = [0, -1]  # Eliminación de la referencia a GROUP_NUMBER

@app.get("/data_train")
async def read_data():
    global timestamps

    if timestamps[1] >= 6:
        raise HTTPException(status_code=400, detail="Ya se recolectó toda la información mínima necesaria")

    current_time = time.time()
    last_update_time = timestamps[0]

    if current_time - last_update_time > MIN_UPDATE_TIME:
        timestamps[0] = current_time
        timestamps[1] += 1

    random_data = get_batch_data(timestamps[1])
    with open("Diabetes/timestamp/timestamps.json", "w") as file:
        file.write(json.dumps(timestamps))

    return {"batch_number": timestamps[1] + 1, "data": random_data}

@app.get("/data_validation")
async def read_data_validation():
    return {"data": validation_data}

@app.get("/data_test")
async def read_data_test():
    return {"data": test_data}

@app.get("/restart_data_generation")
async def restart_data():
    timestamps[0] = 0
    timestamps[1] = -1
    with open("Diabetes/timestamp/timestamps.json", "w") as file:
        file.write(json.dumps(timestamps))
    return {"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
