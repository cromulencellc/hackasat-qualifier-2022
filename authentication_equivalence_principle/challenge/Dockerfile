FROM python:3.8-slim


# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   python3-virtualenv \
                   python-dev \
                   build-essential \
                   python3-pip \
                   python3-setuptools 


#
WORKDIR /temp
COPY requirements.txt /temp
RUN pip3 install --no-cache-dir -r requirements.txt

# 
WORKDIR /challenge
ADD *.py /challenge/ 



ADD data.tle /challenge
CMD ["python3", "challenge.py"]
