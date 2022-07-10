FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get install -y build-essential
RUN apt-get install -y python3-dev libpq-dev
RUN apt-get install -y isort black
WORKDIR /usr/src/app/MovieWordCloud
COPY . .
RUN python setup.py install
