FROM python:3.8-slim AS python_env


# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   python3-virtualenv \
                   python3-dev \
                   python3-tk \  
                   python3-pip \
                   python3-setuptools \
                   git \
                   build-essential \
                   qemu-user \
                   qemu-user-static \
                   gcc-aarch64-linux-gnu \
                   binutils-aarch64-linux-gnu \
                   binutils-aarch64-linux-gnu-dbg \
                   swig

WORKDIR /src
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:/home/xqemu:$PATH"
COPY reqs.txt /home/challenge/
# Pip install some other stuff
RUN python3 -m venv ${VIRTUAL_ENV} ;\ 
    pip3 install build; \
    pip3 install -r /home/challenge/reqs.txt 
RUN git clone https://bitbucket.org/avslab/basilisk.git /home/basilisk 

RUN cd /home/basilisk ; python3 conanfile.py 

COPY ./sim/*.py /home/challenge/sim/
COPY ./fsw/*.py /home/challenge/fsw/
COPY ./*.py /home/challenge/
COPY ./templates/*.html /home/challenge/templates/

# Make the folders we need
WORKDIR /home/challenge
RUN mkdir /home/challenge/web
RUN mkdir /home/challenge/static
RUN mkdir /home/challenge/tmp
ENV PATH="/opt/venv/bin:/home/xqemu/bin:$PATH"

EXPOSE 7100

RUN apt-get install tini
COPY *.sh /home/challenge/

RUN groupadd -r --gid=1000 challenge && \
    useradd -m -r -s /bin/bash -g challenge --uid=1000 challenge && \
    chown -R challenge /home/challenge && \
    chgrp -R challenge /home/challenge 

RUN groupadd -r --gid=2000 qemu && \
    useradd -m -r -s /bin/bash -g qemu --uid=2000 qemu &&\
    passwd -d qemu &&\
    chmod 770 /home/challenge/*.py  &&\
    chmod 770 /home/challenge/fsw/*.py &&\ 
    chmod 770 /home/challenge/sim/*.py  



CMD ["/usr/bin/tini", "--", "/home/challenge/run.sh"]

