FROM ubuntu:jammy

MAINTAINER thomasbechtold@jpberlin.de

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APPDIR /app

RUN apt update \
    && apt install --no-install-recommends --yes python3-pip gcc libpython3-dev libmariadb-dev pkg-config

WORKDIR $APPDIR

COPY . .
RUN cd django-kitamanager && pip3 install --no-cache-dir "." gunicorn tzdata

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8000
CMD gunicorn kmsite.wsgi:application --bind 0.0.0.0:8000
