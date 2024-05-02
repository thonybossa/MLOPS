import requests
import pandas as pd
# URL del endpoint
url = 'http://localhost/restart_data_generation'

# Realizar la solicitud GET

response = requests.get(url)
print(response)
data = response.json()  # Esto convierte el JSON en un diccionario Python
print(data)
df = pd.DataFrame(data)  # E

# Imprimir el contenido de la respuesta
print(df.head())
print(len(df))   
print(df.columns)