FROM python:3.8-slim AS python_env


# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   python3-virtualenv \
                   python3-dev \
                   python3-tk \  
                   python3-pip \
                   python3-setuptools 
WORKDIR /src
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:/home/xqemu:$PATH"
COPY reqs.txt /home/challenge/
# Pip install some other stuff
RUN python3 -m venv ${VIRTUAL_ENV} ;\ 
    pip3 install build; \
    pip3 install -r /home/challenge/reqs.txt 


FROM python:3.8-slim

ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
# Copy only teh stuff we care about
COPY --from=python_env /opt/venv /opt/venv
EXPOSE 7100

WORKDIR /challenge

COPY *.py /challenge/
COPY templates/* /challenge/templates/

CMD ["python3","challenge.py"]