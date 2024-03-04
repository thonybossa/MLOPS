
# Definimos las claves de características que se escalarán utilizando el método MinMaxScaler.
SCALE_MINMAX_FEATURE_KEYS = [
        "Horizontal_Distance_To_Hydrology",
        "Vertical_Distance_To_Hydrology",
    ]

# Definimos las claves de características que se escalarán a un rango entre 0 y 1.
SCALE_01_FEATURE_KEYS = [
        "Hillshade_9am",
        "Hillshade_Noon",
        "Horizontal_Distance_To_Fire_Points",
    ]

# Definimos las claves de características que se escalarán utilizando el método StandardScaler.
SCALE_Z_FEATURE_KEYS = [
        "Elevation",
        "Slope",
        "Horizontal_Distance_To_Roadways",
    ]

# Definimos las claves de características cuyos valores son categóricos y se utilizará un vocabulario para su representación.
VOCAB_FEATURE_KEYS = ["Wilderness_Area"]

# Definimos las claves de características cuyos valores son representados como una cadena de caracteres y se utilizará un hash para su representación.
HASH_STRING_FEATURE_KEYS = ["Soil_Type"]

# Clave de la etiqueta de clasificación.
LABEL_KEY = "Cover_Type"

# Función de utilidad para renombrar la característica transformada.
def transformed_name(key):
    return key + '_xf'
