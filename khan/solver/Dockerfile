FROM python:3.9-slim

RUN apt-get -y update && apt-get -y upgrade &&\
    apt-get -y install bsdiff

COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Copy challenge files
WORKDIR /solver
COPY solve* /solver/

# Add less privledged user and change to them
RUN groupadd -r --gid=1000 solver && \
    useradd -m -r -s /bin/bash -g solver --uid=1000 solver && \
    mkdir -p /solver && \
    chown -R solver /solver && \
    chgrp -R solver /solver 
USER solver

VOLUME /data/

CMD ["sh", "solve.sh"]
