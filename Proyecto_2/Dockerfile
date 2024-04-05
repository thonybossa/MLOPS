FROM python:3.9
ARG MLFLOW_S3_ENDPOINT_URL=http://10.43.101.152:8088
ARG AWS_ACCESS_KEY_ID=minioadmin
ARG AWS_SECRET_ACCESS_KEY=minioadmin
RUN mkdir /work
WORKDIR /work
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8083
ENTRYPOINT ["mlflow", "server", "--host", "0.0.0.0", "--default-artifact-root", "s3://mlflow/"]