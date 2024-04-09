#Creacion de la imagen de jupyter
FROM python:3.9
ARG MLFLOW_S3_ENDPOINT_URL=http://10.43.101.152:8089
ARG AWS_ACCESS_KEY_ID=minioadmin
ARG AWS_SECRET_ACCESS_KEY=minioadmin
RUN mkdir /work
WORKDIR /work
COPY . /work
COPY ./requirements.txt /requirements.txt
RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1
RUN pip install -r requirements.txt
#Exposicion del puerto 8086
EXPOSE 8086

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root", "--port", "8086"]