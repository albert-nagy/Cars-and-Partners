FROM python:3.6

LABEL maintainer "Albert Nagy <nagy.albert@hotmail.com>"

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000