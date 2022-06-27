FROM python:3.8-slim AS python_env 

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
             software-properties-common \
            python3-virtualenv \
            python-dev \
            python3-pip 

ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV ;\
    pip install --upgrade pip ;


FROM ubuntu:focal

# Copy stuff from python env
COPY --from=python_env /opt/venv /opt/venv

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends software-properties-common && \
    apt-get update && \
    add-apt-repository ppa:gnuradio/gnuradio-releases &&\
    apt-get update -y &&\
    apt-get install gnuradio -y

WORKDIR /challenge
COPY *.py /challenge/
COPY spacejam.txt /challenge/

EXPOSE 12001/tcp
COPY gnuradio-runtime.conf /etc/gnuradio/conf.d/
RUN apt-get install -y tini
COPY runme.sh /challenge/
COPY spacejam_music.m4a /challenge/
CMD ["/usr/bin/tini", "--", "/challenge/runme.sh"]

#CMD  ["python3", "challenge.py", "--sample-port","12001"  ]
