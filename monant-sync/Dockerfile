FROM python:3.7.4-slim-buster

WORKDIR /app

COPY sync ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "/app/sync.py"]