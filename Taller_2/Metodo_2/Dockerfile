FROM tensorflow/tfx:1.12.0

WORKDIR /tfx/src

COPY . .

RUN pip install apache-beam[interactive]==2.45.0
RUN pip install -r requirements.txt

ENTRYPOINT ["/run_jupyter.sh"]
