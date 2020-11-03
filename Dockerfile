FROM python:3.6

# Fiona requires Python versions 3.6+ and GDAL version 1.11-3.0 with GDAL_VERSION specified
ENV GDAL_VERSION=3.0

RUN apt-get -y update;  apt -y install software-properties-common 
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get -y install gdal-bin python3-gdal libspatialindex-dev

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /data
