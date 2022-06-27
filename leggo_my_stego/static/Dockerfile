FROM python:3.10-slim

VOLUME /data/
WORKDIR /images
COPY  images/*.jpg /images/
COPY *.sh .
CMD /bin/sh copy.sh