import os
import sys
import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# Comprobar e instalar dependencias necesarias
def install(package):
    os.system(f"{sys.executable} -m pip install {package}")

# Listar las dependencias
dependencies = ['pandas', 'numpy', 'scikit-learn', 'requests']

# Instalar las dependencias si no están ya instaladas
for dep in dependencies:
    try:
        __import__(dep)
    except ImportError:
        install(dep)

# Define the root directory
_data_root = '../Diabetes'
_data_filepaths = os.path.join(_data_root, 'Diabetes.csv')

#Download the data
os.makedirs(_data_root, exist_ok=True)
if not os.path.isfile(_data_filepaths):
    url = 'https://docs.google.com/uc?export= \
        download&confirm={{VALUE}}&id=1k5-1caezQ3zWJbKaiMULTGq-3sz6uThC'
    r = requests.get(url, allow_redirects=True, stream=True)
    open(_data_filepaths, 'wb').write(r.content)

# Load the data
df = pd.read_csv(_data_filepaths)

# Split the data into features and labels
data = df.values
etiquetas = df['readmitted'].values

# Divide data into training, validation, and test sets
df_train_data, test_validation_data, train_labels, test_validation_labels = train_test_split(
    data, etiquetas, train_size=0.8843818171098402, random_state=42
)

#Divide the test/validation data into test and validation
df_test_data, df_validation_data, test_labels, validation_labels = train_test_split(
    test_validation_data, test_validation_labels, test_size=0.5, random_state=42
)

# Convertir numpy arrays de vuelta a DataFrame para poder usar to_csv
df_train = pd.DataFrame(df_train_data, columns=df.columns)
df_test = pd.DataFrame(df_test_data, columns=df.columns)
df_validation = pd.DataFrame(df_validation_data, columns=df.columns)

# Guardar los DataFrames en archivos CSV
df_train.to_csv('../Diabetes/df_train_data.csv', index=False)
df_test.to_csv('../Diabetes/df_test_data.csv', index=False)
df_validation.to_csv('../Diabetes/df_validation_data.csv', index=False)