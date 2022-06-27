FROM python:3-alpine 
RUN pip install six pysocks
RUN mkdir /solver

WORKDIR /solver
ADD pwnlib /solver/pwnlib
ADD solver.py hints.json /solver/

CMD ["python", "solver.py"]
