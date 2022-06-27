FROM python:3.10

RUN apt update -y && \
    apt install -y xxd tini

ADD requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir -p /app/flag && \
    chown -R 1000:1000 /app

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

USER 1000:1000
WORKDIR /app

COPY screamingfist.py .

CMD ["/usr/bin/tini", "--", "/entrypoint.sh"]

