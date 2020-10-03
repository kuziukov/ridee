FROM python:3.6.6-alpine3.8

COPY requirements.txt .

RUN apk add libffi-dev g++ --no-cache && \
    pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /code/

COPY ./src/ /code/