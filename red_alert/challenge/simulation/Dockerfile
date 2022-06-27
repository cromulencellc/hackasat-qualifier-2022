FROM python:3.8-slim AS python_env

WORKDIR /src
RUN apt update ;\
    apt install -y --no-install-recommends python3-virtualenv python-dev build-essential
    
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY reqs.txt ./

RUN python -m venv $VIRTUAL_ENV ;\
    pip3 install --upgrade pip ;\
    pip3 install --no-cache-dir -r reqs.txt


FROM python:3.8-slim
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=python_env /opt/venv /opt/venv
EXPOSE 5000

WORKDIR /simulation
COPY *.py /simulation/
COPY *.bsp /simulation/
COPY *.yml /simulation/
COPY *.tle /simulation/
CMD ["python3","webhook.py"]