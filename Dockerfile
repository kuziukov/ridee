FROM python:3.7.9-alpine3.12

COPY requirements.txt .

RUN apk add libffi-dev g++ --no-cache && \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /code/

COPY ./src/ /code/