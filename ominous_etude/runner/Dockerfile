FROM python:3-alpine

RUN apk add qemu-microblaze file socat

RUN mkdir -p /challenge
RUN addgroup -g 1000 challenge
RUN adduser -u 1000 -G challenge -D challenge

ADD ominous_etude.tar.bz2 lib.tar.bz2 runner.py timeout.py /challenge/

USER challenge:challenge

WORKDIR /challenge

CMD ["python3", "/challenge/runner.py"]
