FROM python:3-alpine

RUN apk add qemu-microblaze file socat

RUN addgroup -g 1000 challenge
RUN adduser -u 1000 -G challenge -D challenge

ADD blazing_etudes.tar.bz2 /challenge/
ADD microblaze-linux.tar.bz2 /opt/cross/

ADD runner.py timeout.py /challenge/

USER challenge:challenge

WORKDIR /challenge

CMD ["python3", "/challenge/runner.py"]
