FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/MovieWordCloud
COPY . .
RUN python setup.py install

CMD tail -f /dev/null
