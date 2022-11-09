FROM continuumio/miniconda3
MAINTAINER Ryan Keogh

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=djangoGeo.settings

RUN apt-get -y update && apt-get -y upgrade
RUN conda update -n base conda && conda update -n base --all

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get -y install build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

COPY ENV.yml /usr/src/app
RUN conda env create -n djangoGeo --file ENV.yml

RUN echo "conda activate djangoGeo" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN conda config --add channels conda-forge && conda config --set channel_priority strict
RUN cat ~/.condarc
RUN conda install gunicorn

COPY . /usr/src/app

RUN python manage.py collectstatic --no-input

EXPOSE 8002

CMD gunicorn djangoGeo.wsgi --config gunicorn.conf.py