import streamlit as st
import requests

# Define la URL de tu servidor FastAPI
FASTAPI_URL = 'http://10.43.101.152:8085'

# Define una función para hacer una solicitud de predicción a tu API de FastAPI
def get_prediction(data):
    response = requests.post(f"{FASTAPI_URL}/predict", json=data)
    prediction = response.json()
    return prediction

# Define la interfaz de usuario de la aplicación Streamlit
def main():
    # Configure the Streamlit page layout
    st.set_page_config(layout="wide")

    st.title(':computer: Proyecto 3 MLOPS: Grupo 3 :computer:')
    st.subheader(
        "En este dashboard, encontrará toda la información relacionada con el proyecto 3 de la materia MLOPS"
    )
    st.sidebar.title("Integrantes")
    st.sidebar.write(
        """
        Anthony Bossa \n
        Jose Luis Vega \n
        Víctor De La Hoz
        """
    )
    st.divider()
    st.header(f"Links de interés")
    st.markdown("En esta sección podrá dirigirse tanto al repositorio del equipo como a las direcciones donde estan dispuestos los servicios integrados en la solución")
    _, col2, _, col4, _, col6, _ = st.columns([1, 5, 1, 5, 1, 5, 1])
    with col2:
        st.link_button("Repositorio del equipo", "https://github.com/thonybossa/MLOPS")
    with col4:
        st.link_button("MLFLOW", "http://10.43.101.152:8083")
    with col6:
        st.link_button("AirFlow", "http://10.43.101.152:8080")
    st.divider()
    cols = st.columns(4)



    # Define los campos de entrada
    race = cols[0].text_input("Race", value="AfricanAmerican")
    gender = cols[1].text_input("Gender", value="Female")
    age = cols[2].text_input("Age", value="[60-70)")
    admission_type_id = cols[3].text_input("Admission Type ID", value="1")
    discharge_disposition_id = cols[0].text_input("Discharge Disposition ID", value="3")
    admission_source_id = cols[1].text_input("Admission Source ID", value="5")
    time_in_hospital = cols[2].text_input("Time in Hospital", value="7")
    medical_specialty = cols[3].text_input("Medical Specialty", value="Nephrology")
    num_lab_procedures = cols[0].text_input("Number of Lab Procedures", value="47")
    num_procedures = cols[1].text_input("Number of Procedures", value="2")
    num_medications = cols[2].text_input("Number of Medications", value="29")
    number_emergency = cols[3].text_input("Number of Emergency Visits", value="0")
    number_inpatient = cols[0].text_input("Number of Inpatient Visits", value="1")
    diag_1 = cols[1].text_input("Primary Diagnosis", value="38")
    diag_2 = cols[2].text_input("Secondary Diagnosis", value="263")
    diag_3 = cols[3].text_input("Additional Diagnosis", value="403")
    number_diagnoses = cols[0].text_input("Number of Diagnoses", value="9")
    insulin = cols[1].text_input("Insulin", value="Steady")
    change = cols[2].text_input("Change", value="Ch")
    diabetesMed = cols[3].text_input("Diabetes Medication", value="Yes")
    
    # Crea un botón para realizar la predicción
    if st.button('Predict'):
        # Hace una solicitud de predicción a tu API de FastAPI
        data = {
            "race": race,
            "gender": gender,
            "age": age,
            "admission_type_id": admission_type_id,
            "discharge_disposition_id": discharge_disposition_id,
            "admission_source_id": admission_source_id,
            "time_in_hospital": time_in_hospital,
            "medical_specialty": medical_specialty,
            "num_lab_procedures": num_lab_procedures,
            "num_procedures": num_procedures,
            "num_medications": num_medications,
            "number_emergency": number_emergency,
            "number_inpatient": number_inpatient,
            "diag_1": diag_1,
            "diag_2": diag_2,
            "diag_3": diag_3,
            "number_diagnoses": number_diagnoses,
            "insulin": insulin,
            "change": change,
            "diabetesMed": diabetesMed
        }
        prediction = get_prediction(data)
        
        # Muestra el resultado de la predicción
        st.write('Prediction:', prediction['prediction'])

if __name__ == '__main__':
    main()
