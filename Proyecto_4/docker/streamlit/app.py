import streamlit as st
import requests

# Define la URL de tu servidor FastAPI
#FASTAPI_URL = 'http://10.43.101.152:8085'
FASTAPI_URL = 'http://fastapi:8085'

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
        "En este dashboard, encontrará toda la información relacionada con el proyecto 4 de la materia MLOPS"
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
    status = cols[0].text_input("Status", value="for_sale")
    bed = cols[1].number_input("Bed", value=4.0)
    bath = cols[2].number_input("Bath", value=2.0)
    acre_lot = cols[3].number_input("Acre Lot", value=0.38)
    state = cols[0].text_input("State", value="Conneticut")
    house_size = cols[1].number_input("House Size", value=1617)
    
    # Crea un botón para realizar la predicción
    if st.button('Predict'):
        # Hace una solicitud de predicción a tu API de FastAPI
        data = {
            "status": status,
            "bed": bed,
            "bath": bath,
            "acre_lot": acre_lot,
            "state": state,
            "house_size": house_size,
            
        }
        prediction = get_prediction(data)
        
        # Muestra el resultado de la predicción
        st.write('Prediction:', prediction['prediction'])

if __name__ == '__main__':
    main()