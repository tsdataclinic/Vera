FROM python

RUN apt-get -y update;  apt -y install software-properties-common 
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get -y install gdal-bin python3-gdal libspatialindex-dev

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
