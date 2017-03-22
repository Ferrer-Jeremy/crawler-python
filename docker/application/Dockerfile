FROM python:latest
# While we are in dev. Change to alpine, slim or even a custom image

RUN apt-get update \
    && apt-get install -y \
        firefox-esr \
        xvfb

#RUN add-apt-repository ppa: \
#    && apt-get update \
#    && apt-get install -y \
#        chroumium



ADD . /var/www
WORKDIR /var/www
RUN usermod -u 1000 www-data
# We need to update pip
# The requirement must be in a fixed version
RUN pip install -r requirements.txt