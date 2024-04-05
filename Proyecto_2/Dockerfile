FROM python:3.9
ARG MLFLOW_S3_ENDPOINT_URL=http://http://10.43.101.152/:8084
ARG AWS_ACCESS_KEY_ID=minioadmin
ARG AWS_SECRET_ACCESS_KEY=minioadmin
RUN mkdir /work
WORKDIR /work
COPY . .
RUN pip install jupyter==1.0.0 -U && pip install jupyterlab==3.6.1
RUN pip install -r requirements.txt
EXPOSE 8888
ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]