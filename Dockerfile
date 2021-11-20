FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update \
# && apt-get install -y --no-install-recommends git \
# && apt-get purge -y --auto-remove \
# && rm -rf /var/lib/apt/lists/*

#RUN git clone git://github.com/Bgeninatti/MovieWordCloud.git
WORKDIR /usr/src/app/MovieWordCloud
COPY . .
RUN cp mwc/cfg.py.bak mwc/cfg.py
RUN python setup.py install

CMD tail -f /dev/null
