FROM python:3.10

RUN mkdir -p /app/images && \
    chown -R 1000:1000 /app


COPY entrypoint.sh /

USER 1000:1000
WORKDIR /app

COPY *.py /app/

CMD /entrypoint.sh