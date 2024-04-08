# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
RUN mkdir /work
WORKDIR /work

# Copy the current directory contents into the container at /app
COPY . /work

COPY ./requirements.txt /requirements.txt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8083 available to the world outside this container
EXPOSE 8083

# Run mlflow server when the container launches
CMD ["python3", "-m", "mlflow", "server", \
     "--backend-store-uri", "mysql+mysqldb://ab:ab@mysql/Base_de_Datos", \
     "--default-artifact-root", "minio://proyecto-2", \
     "--host", "0.0.0.0:8083", \
     "--serve-artifacts"]

