from pydantic import BaseModel

class PenguinData(BaseModel):
    studyName: str = "PAL0708"
    Sample_Number: int = 1
    Region: str = "Anvers"
    Island: str = "Torgersen"
    Stage: str = "Adult, 1 Egg Stage"
    Individual_ID: str = "N1A1"
    Clutch_Completion: str = "Yes"
    Date_Egg: str = "11/11/07"
    Culmen_Length_mm: float = 39.1
    Culmen_Depth_mm: float = 18.7
    Flipper_Length_mm: float = 181.0
    Body_Mass_g: float = 3750.0
    Sex: str = "Male"
    Delta_15_N: str = "NaN"
    Delta_13_C: str = "NaN"
