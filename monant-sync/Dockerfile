FROM python:3.8.0-slim-buster

WORKDIR /app

COPY sync ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-u", "/app/run.py"]