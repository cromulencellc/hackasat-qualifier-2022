FROM python:3.9-slim

RUN apt-get -y update && apt-get upgrade -y && apt -y install \
    tini

COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Copy challenge files
WORKDIR /chal/libs/
COPY libs /chal/libs/

WORKDIR /chal
COPY run.sh /chal/
COPY chal.py /chal/

# Add less privledged user and change to them
RUN groupadd -r --gid=1000 challenge && \
    useradd -m -r -s /bin/bash -g challenge --uid=1000 challenge && \
    mkdir -p /chal && \
    chown -R challenge /chal && \
    chgrp -R challenge /chal && \
    chmod +x /chal/run.sh

USER challenge


CMD ["/usr/bin/tini", "--", "/chal/run.sh"]
