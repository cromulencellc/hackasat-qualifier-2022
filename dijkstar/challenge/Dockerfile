FROM python:3.8-slim AS python_env

RUN apt update ;\
    apt install -y --no-install-recommends python3-virtualenv python-dev build-essential
    
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV ;


FROM python:3.8-slim
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=python_env /opt/venv /opt/venv

COPY / /challenge/

WORKDIR /challenge

CMD ["python", "challenge.py"]
