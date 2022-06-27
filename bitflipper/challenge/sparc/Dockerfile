FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt -y upgrade && apt -y install \
    qemu-user \
    tini \
    python3

WORKDIR /challenge

COPY challenge/sparc/run.sh /challenge/
COPY static/bin/* /challenge/

# Add less privledged user and change to them
RUN groupadd -r --gid=1000 challenge && \
    useradd -m -r -s /bin/bash -g challenge --uid=1000 challenge
USER challenge

WORKDIR /challenge

ENTRYPOINT [ "tini", "--", "/challenge/run.sh" ]
