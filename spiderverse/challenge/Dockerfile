FROM python:3.8-slim AS python_env


RUN apt update ;\
    apt install -y --no-install-recommends python3-virtualenv python-dev build-essential
    
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY reqs.txt ./

RUN python3 -m venv $VIRTUAL_ENV ;\
    pip3 install --upgrade pip ;\
    pip3 install --no-cache-dir -r reqs.txt




# Install crosslinks 

FROM python:3.8-slim
ENV DEBIAN_FRONTEND noninteractive

# Copy our python junk over into this container
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
COPY --from=python_env /opt/venv /opt/venv



WORKDIR  /challenge

# Make a new user and give it permissions
#RUN groupadd -r --gid=1000 challenge && \
#    useradd -m -r -s /bin/bash -g challenge --uid=1000 challenge && \
#    mkdir -p /challenge && \
#    chown -R challenge /challenge && \
#    chgrp -R challenge /challenge 
#USER challenge
#

RUN apt update; apt-get install -y tini


COPY *.py /challenge/
COPY *.sh /challenge/
EXPOSE 5000
CMD ["/usr/bin/tini", "--", "/challenge/runme.sh"]
#CMD ["python3" ,  "challenge.py"]
