FROM python:3.8-slim AS python_env


# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   python3-virtualenv \
                   python-dev \
                   build-essential \
                   python3-pip \
                   python3-setuptools 
WORKDIR /src
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt ./
# Pip install some other stuff
RUN python3 -m venv ${VIRTUAL_ENV} ;\ 
    pip3 install build;\
    pip3 install --no-cache-dir -r requirements.txt

# Install crosslinks 

FROM python:3.8-slim
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"
# Copy only teh stuff we care about
COPY --from=python_env /opt/venv /opt/venv

# Build and install crosslink as a package
WORKDIR /temp
COPY ./ /temp

RUN python3 -m build &&\
    pip3 install dist/*.whl &&\
    rm -rf /temp
