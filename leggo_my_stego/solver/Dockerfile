FROM python:3.10-slim

RUN pip install pwn
RUN apt-get update && apt-get install -y steghide


RUN mkdir /solver/
RUN mkdir /solver/images
RUN mkdir /solver/work
WORKDIR /solver

COPY solver.py /solver
COPY *.txt /solver/
CMD python ./solver.py --images /solver/images
