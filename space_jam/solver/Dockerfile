FROM ubuntu:focal



RUN apt-get update -y && \
    apt-get install -y --no-install-recommends software-properties-common && \
    apt-get update && \
    add-apt-repository ppa:gnuradio/gnuradio-releases &&\
    apt-get update -y &&\
    apt-get install gnuradio -y && \
    apt-get install python3-pip -y

COPY reqs.txt ./
# Pip install some other stuff
RUN python3 -m venv ${VIRTUAL_ENV} ;\ 
    pip3 install build;\
    pip3 install --no-cache-dir -r reqs.txt


WORKDIR /solver
COPY *.py /solver/
COPY *.json /solver/



CMD  ["python3", "solver.py", "--tx-config","psk_8.json","--rx-config","rx_narrow.json"  ]
