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
