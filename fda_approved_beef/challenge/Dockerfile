FROM nestybox/ubuntu-focal-systemd-docker

# Get curl which will be used by build-containers.sh
RUN apt-get update && apt-get install -y \
  curl \
  gettext-base \
  make \
  && apt-get clean autoclean \ 
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /build
WORKDIR /build
COPY ./fprime-challenge /build/fprime-challenge
COPY ./Makefile /build
COPY install-compose.sh /build/
RUN /bin/bash /build/install-compose.sh
COPY build_containers.sh /usr/bin
RUN build_containers.sh 
RUN rm -rf /build

RUN mkdir /challenge
WORKDIR /challenge
COPY docker-compose.yml /challenge/
COPY run.sh /challenge/
# COPY challenge.service /etc/systemd/system/challenge.service
# RUN systemctl enable challenge.service
EXPOSE 5000
EXPOSE 5001


