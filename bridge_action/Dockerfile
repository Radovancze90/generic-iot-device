FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN pip install --no-cache-dir mysql-connector-python paho-mqtt

CMD [ "python", "/usr/src/app/main.py" ]
