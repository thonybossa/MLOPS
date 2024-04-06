FROM python:3.9

# Variables de entorno para MLflow
ENV MLFLOW_S3_ENDPOINT_URL=http://10.43.101.152:8088
ARG AWS_ACCESS_KEY_ID=minioadmin
ARG AWS_SECRET_ACCESS_KEY=minioadmin

# Crear directorio de trabajo
RUN mkdir /work
WORKDIR /work

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install -r requirements.txt

# Exponer puerto para MLflow
EXPOSE 8083

# Comando para iniciar MLflow
CMD mlflow server --host 0.0.0.0 --port 8083 --default-artifact-root s3://mlflows3/artifacts --backend-store-uri sqlite:////mlflow.db --serve-artifacts