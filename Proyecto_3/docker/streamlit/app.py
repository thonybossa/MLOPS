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

    st.title(':computer: Proyecto 2 MLOPS: Grupo 3 :computer:')
    st.subheader(
        "En este dashboard, encontrará toda la información relacionada con el proyecto 2 de la materia MLOPS"
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
    elevation = cols[0].number_input("Elevation",value=3154)
    aspect = cols[1].number_input("Aspect", value=351)
    slope = cols[2].number_input("Slope", value=13)
    horizontal_distance_to_hydrology = cols[3].number_input("Horizontal Distance To Hydrology", value=150)
    vertical_distance_to_hydrology = cols[0].number_input("Vertical Distance To Hydrology", value=31)
    horizontal_distance_to_roadways = cols[1].number_input("Horizontal Distance To Roadways", value=2023)
    hillshade_9am = cols[2].number_input("Hillshade 9am", value=196)
    hillshade_noon = cols[3].number_input("Hillshade Noon", value=217)
    hillshade_3pm = cols[0].number_input("Hillshade 3pm", value=159)
    horizontal_distance_to_fire_points = cols[1].number_input("Horizontal Distance To Fire Points", value=1828)
    wilderness_area = cols[2].text_input("Wilderness Area", value='Rawah')  
    soil_type = cols[3].text_input("Soil Type", value='C7745')  
    
    # Crea un botón para realizar la predicción
    if st.button('Predict'):
        # Hace una solicitud de predicción a tu API de FastAPI
        data = {
            "Elevation": elevation,
            "Aspect": aspect,
            "Slope": slope,
            "Horizontal Distance To Hydrology": horizontal_distance_to_hydrology,
            "Vertical Distance To Hydrology": vertical_distance_to_hydrology,
            "Horizontal Distance To Roadways": horizontal_distance_to_roadways,
            "Hillshade 9am": hillshade_9am,
            "Hillshade Noon": hillshade_noon,
            "Hillshade 3pm": hillshade_3pm,
            "Horizontal Distance To Fire Points": horizontal_distance_to_fire_points,
            "Wilderness Area": wilderness_area,
            "Soil Type": soil_type,
        }
        prediction = get_prediction(data)
        
        # Muestra el resultado de la predicción
        st.write('Prediction:', prediction['prediction'])

if __name__ == '__main__':
    main()
