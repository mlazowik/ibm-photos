FROM python:3-slim

LABEL maintainer="mlazowik@gmail.com"

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git

ENV BACK_ROOT /opt/back
RUN mkdir -p $BACK_ROOT
WORKDIR $BACK_ROOT

COPY back/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install uwsgi

COPY back .

ENV DJANGO_SETTINGS_MODULE="photos.settings"

EXPOSE 8000

ENTRYPOINT ["sh", "/opt/back/entrypoint.sh"]
