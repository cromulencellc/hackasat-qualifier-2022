FROM python:3.8-slim AS python_env
WORKDIR /src
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   python3-virtualenv \
                   python-dev \
                   build-essential \
                   python3-pip \
                   python3-setuptools 

COPY requirements.txt ./


RUN python3 -m venv ${VIRTUAL_ENV} ;\ 
    pip3 install --no-cache-dir -r requirements.txt

FROM python:3.8-slim
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=python_env /opt/venv /opt/venv

WORKDIR /solve
ADD *.py /solve/
CMD ["python3" , "solver.py"]