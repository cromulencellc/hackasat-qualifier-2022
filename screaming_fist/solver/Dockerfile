FROM python:3.10

RUN apt update -y && \
    apt install -y xxd

ADD requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /app && \
    chown -R 1000:1000 /app

USER 1000:1000
WORKDIR /app

COPY solver.py ./

CMD python ./solver.py $HOST $PORT $SERVICE_HOST $SERVICE_PORT
