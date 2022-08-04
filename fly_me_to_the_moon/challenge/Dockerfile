FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt upgrade -y && \
    apt update -y && \
    apt install -y wget \
                   tar \
                   python3 \
                   python3-pip \
                   npm

WORKDIR /challenge

# Get and unpack gmat

RUN wget https://sourceforge.net/projects/gmat/files/GMAT/GMAT-R2020a/gmat-ubuntu-x64-R2020a.tar.gz/download && \
    tar xvf download
# Update NODE
RUN npm cache clean -f &&\
    npm install -g n &&\
    n stable 

COPY requirements.txt ./
RUN pip3 install -r requirements.txt




COPY ./viewer /challenge/viewer/
RUN cd /challenge/viewer &&\
    npm install &&\
    npm run build

COPY ./*.py /challenge/
COPY *.sh /challenge/
COPY *.txt /challenge/
COPY ./gmat_scripts /challenge/gmat_scripts

EXPOSE 8080

RUN apt-get install tini
CMD ["/usr/bin/tini", "--", "/challenge/startup.sh"]

