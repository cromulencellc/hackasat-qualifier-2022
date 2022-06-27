FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        pip \
        software-properties-common

RUN pip install --upgrade pip ;\
    pip install --no-cache-dir \
        timeout

RUN add-apt-repository ppa:gnuradio/gnuradio-releases && \
    apt update && \
    apt install -y --no-install-recommends gnuradio

RUN volk_profile

WORKDIR /solver
COPY solver_nogui.py solver.sh /solver/

CMD ["/bin/bash", "solver.sh"]
