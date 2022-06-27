FROM ubuntu:20.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt -y upgrade && apt -y install \
    build-essential \
    gcc-10-sparc64-linux-gnu \
    gcc-multilib-sparc64-linux-gnu \
    lib32gcc-10-dev-sparc64-cross

# Add less privledged user and change to them
RUN groupadd -r --gid=1000 gen && \
    useradd -m -r -s /bin/bash -g gen --uid=1000 gen
USER gen

WORKDIR /static

ENTRYPOINT [ "make", "clean", "all"]
