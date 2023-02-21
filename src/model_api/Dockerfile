FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential vim python3.10 python3-pip python3-setuptools python3-dev

WORKDIR /app

COPY src/model_api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src/model_api/ /app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]