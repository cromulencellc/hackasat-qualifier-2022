FROM registry.mlb.cromulence.com/has3/quals/fprime-exploitation/challenge-ground:latest

USER root

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get  install  -y \
        python3 \
        binutils \ 
        wget \
        jq \
        sed \
        net-tools \
        iputils-ping \
        netcat \
        # firefox-esr \
        && apt-get clean autoclean \ 
        && rm -rf /var/lib/apt/lists/*

WORKDIR ${GROUND_DIR}


ENV VIRTUAL_ENV=${GROUND_DIR}/fprime-venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY solver.sh solver.py ${GROUND_DIR}/
COPY genprime.py ${GROUND_DIR}/
RUN chmod +x ${GROUND_DIR}/solver.sh
USER ground

# ENTRYPOINT [ "/bin/bash", "./solver.sh"]

ENTRYPOINT [ "python3", "./solver.py" ]