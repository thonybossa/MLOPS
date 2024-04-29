FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
COPY main/read_data_api.py read_data_api.py

EXPOSE 8086

CMD ["uvicorn", "read_data_api:app", "--host", "0.0.0.0", "--port", "8086"]
