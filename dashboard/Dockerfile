FROM python:3.9-slim

RUN apt-get update && apt-get install gcc -y && apt-get install g++ -y && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 80