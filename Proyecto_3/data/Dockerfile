FROM python:3.9

COPY requirements.txt requirements.txt
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main/read_data_api.py read_data_api.py

CMD ["uvicorn", "read_data_api:app", "--host", "0.0.0.0", "--port", "8084"]