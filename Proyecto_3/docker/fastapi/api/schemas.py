from pydantic import BaseModel

class PatientData(BaseModel):
    race: str = "AfricanAmerican"
    gender: str = "Female"
    age: str = "[60-70)"
    admission_type_id: str = "1"
    discharge_disposition_id: str = "3"
    admission_source_id: str = "5"
    time_in_hospital: str = "7"
    medical_specialty: str = "Nephrology"
    num_lab_procedures: str = "47"
    num_procedures: str = "2"
    num_medications: str = "29"
    number_emergency: str = "0"
    number_inpatient: str = "1"
    diag_1: str = "38"
    diag_2: str = "263"
    diag_3: str = "403"
    number_diagnoses: str = "9"
    insulin: str = "Steady"
    change: str = "Ch"
    diabetesMed: str = "Yes"
