from locust import HttpUser, task, constant
from pydantic import BaseModel

class CoverType(BaseModel):
    Elevation: int = 3154
    Aspect: int = 351
    Slope: int = 13
    Horizontal_Distance_To_Hydrology: int =150
    Vertical_Distance_To_Hydrology: int = 31
    Horizontal_Distance_To_Roadways: int =2023
    Hillshade_9am: int = 196
    Hillshade_Noon: int = 217
    Hillshade_3pm: int = 159
    Horizontal_Distance_To_Fire_Points: int =1828
    Wilderness_Area: str = "Rawah"
    Soil_Type: str = "C7745"


class LoadTest(HttpUser):
    wait_time = constant(1)
    host = "http://inference:8085"

    @task
    def predict(self):
        request_body = {
            "Elevation": 3154,
            "Aspect": 351,
            "Slope": 13,
            "Horizontal_Distance_To_Hydrology": 150,
            "Vertical_Distance_To_Hydrology": 31,
            "Horizontal_Distance_To_Roadways": 2023,
            "Hillshade_9am": 196,
            "Hillshade_Noon": 217,
            "Hillshade_3pm": 159,
            "Horizontal_Distance_To_Fire_Points": 1828,
            "Wilderness_Area": "Rawah",
            "Soil_Type": "C7745",
            }
        headers = {
            "Content-Type": "application/json",
        }
        self.client.post(
            "/predict", json=request_body, headers=headers
        )