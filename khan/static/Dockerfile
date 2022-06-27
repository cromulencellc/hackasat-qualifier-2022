FROM ubuntu:focal 
ARG DEBIAN_FRONTEND=noninteractive

ARG TZ=Etc/UTC
RUN apt-get update \ 
    && apt-get upgrade -y \
    && apt-get install -y \
    wget \
    ca-certificates \ 
    gcc-aarch64-linux-gnu \
    g++-aarch64-linux-gnu \ 
    binutils-aarch64-linux-gnu \
    binutils-aarch64-linux-gnu-dbg \
    build-essential \
    cmake \
    libeigen3-dev \ 
    && apt-get clean autoclean \ 
    && rm -rf /var/lib/apt/lists/*


WORKDIR /home/builder 

WORKDIR /home/builder 
VOLUME /home/builder/data 
COPY *.py ./
COPY *.cpp ./
COPY CMakeLists.txt ./
COPY buildme.sh ./
COPY includes/ ./includes
COPY *.cmake ./

RUN ["sh" , "buildme.sh"]

ENTRYPOINT [ "cp","/home/builder/build/Lander","/home/builder/data" ]