FROM python:3.9

# Variables de entorno para MLflow
ARG MLFLOW_S3_ENDPOINT_URL=http://10.43.101.152:8088
ARG AWS_ACCESS_KEY_ID=minioadmin
ARG AWS_SECRET_ACCESS_KEY=minioadmin

# Crear directorio de trabajo
RUN mkdir /work
WORKDIR /work

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install -r requirements.txt

# Instalar Jupyter
RUN pip install jupyter

# Exponer puertos para MLflow y Jupyter
EXPOSE 8083 8888

# Comando para iniciar Jupyter y MLflow
CMD jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root & mlflow server --host 0.0.0.0 --port 8083 --default-artifact-root s3://mlflow/