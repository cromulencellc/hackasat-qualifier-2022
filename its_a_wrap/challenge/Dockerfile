FROM python:3.10-slim AS python_env

WORKDIR /src
RUN apt update ;\
    apt install -y --no-install-recommends python3-virtualenv python-dev
    
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./

RUN python -m venv $VIRTUAL_ENV ;\
    pip install --upgrade pip ;\
    pip install --no-cache-dir -r requirements.txt

WORKDIR /challenge
ADD challenge.py /challenge/
COPY ./encrypt /challenge/encrypt

RUN cd /challenge/encrypt && \
    python3 -m compileall -d /challenge -f -o 2 encrypt.py && \
    cd ..

FROM python:3.10-slim as runner
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=python_env /opt/venv /opt/venv

RUN apt update ;\
    apt install -y --no-install-recommends libgfortran5 \
    && apt-get clean autoclean \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY --from=python_env /challenge/encrypt/__pycache__/encrypt.cpython-310.opt-2.pyc /challenge/encrypt.pyc

COPY ./encrypt/libfoo.so /challenge/

COPY ./challenge.py /challenge/

CMD ["python3", "challenge.py"]

FROM debian:bullseye AS generator
WORKDIR /generator
COPY --from=runner /challenge/libfoo.so /generator/challenge/
COPY --from=runner /challenge/encrypt.pyc /generator/challenge/
COPY generator.sh /generator
VOLUME /data
CMD ["sh", "/generator/generator.sh"]
