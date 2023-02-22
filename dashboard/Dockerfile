FROM python:3.9-slim

RUN apt-get update && apt-get install gcc -y && apt-get install g++ -y && apt-get clean
RUN apt-get update && apt-get install gcc -y && apt-get install g++ -y && apt-get clean

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 80