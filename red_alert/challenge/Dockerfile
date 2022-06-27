FROM nestybox/ubuntu-focal-systemd-docker

# Get curl which will be used by build-containers.sh
RUN apt-get update && apt-get install -y \
  curl gettext-base

COPY simulation /challenge/simulation
COPY grafana /challenge/grafana
COPY apicmds /challenge/apicmds
COPY docker-compose.yml /challenge
WORKDIR /challenge

COPY install-compose.sh /challenge/
RUN /challenge/install-compose.sh

COPY build_containers.sh /usr/bin
RUN build_containers.sh 


COPY configure_api.sh /challenge/
COPY configure_contact_points.json /challenge/
COPY start.sh /challenge/
EXPOSE 3000

