FROM ubuntu:18.04 as fprime-builder

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Etc/UTC

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get  install  -y \
        curl \
        build-essential \
        wget \
        jq \
        # cmake \
        python3 \
        python3-pip \
        python3-venv \
        git \
        gdb \
        sudo \
        && apt-get clean autoclean \ 
        && rm -rf /var/lib/apt/lists/*

ARG UID=1000
ARG GID=1000
ARG USERNAME=has

RUN if [ ${UID:-0} -ne 0 ] && [ ${GID:-0} -ne 0 ]; then \
    groupadd -g ${GID} $USERNAME &&\
    useradd -l -m -G sudo -u ${UID} -g $USERNAME $USERNAME; \
    echo "${USERNAME}:${USERNAME}" | chpasswd; \
    fi 

USER $USERNAME

ENV BUILD_DIR=/home/${USERNAME}/fprime

RUN mkdir -p ${BUILD_DIR}

RUN chown -R ${USERNAME}:${USERNAME} ${BUILD_DIR}

WORKDIR ${BUILD_DIR}

RUN git clone --depth=1 --branch v2.1.0 https://github.com/nasa/fprime.git

RUN ln -s fprime/.git .git

ENV VIRTUAL_ENV=${BUILD_DIR}/fprime-venv

RUN python3 -m venv ${VIRTUAL_ENV}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${BUILD_DIR}/fprime/

RUN pip install --upgrade --no-cache-dir \
    cmake \
    wheel \
    setuptools \
    pip \
    sympy \
    fprime-tools \
    fprime-gds

COPY --chown=${USERNAME}:${USERNAME} ./QualsRef ${BUILD_DIR}/QualsRef

WORKDIR ${BUILD_DIR}/QualsRef/

RUN ./build.sh

# ENTRYPOINT [ "bash" ]

FROM ubuntu:18.04 as fprime-space

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Etc/UTC

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get  install  -y \
        python3 \
        python3-pip \
        python3-venv \
        && apt-get clean autoclean \ 
        && rm -rf /var/lib/apt/lists/*

ARG SPACE_UID=1000
ARG SPACE_GID=1000
ARG SPACE_USERNAME=space
ARG BUILD_USERNAME=has
ARG BUILD_EXE_DIR=/home/${BUILD_USERNAME}/fprime
ENV SPACE_DIR=/home/${SPACE_USERNAME}/fsw

RUN if [ ${SPACE_UID:-0} -ne 0 ] && [ ${SPACE_GID:-0} -ne 0 ]; then \
    groupadd -g ${SPACE_GID} $SPACE_USERNAME &&\
    useradd -l -m -u ${SPACE_UID} -g $SPACE_USERNAME $SPACE_USERNAME; \
    fi 

RUN chmod -R o-rwx /home/${SPACE_USERNAME}

COPY --chown=${SPACE_USERNAME}:${SPACE_USERNAME} --from=fprime-builder ${BUILD_EXE_DIR}/QualsRef/build-artifacts/Linux/bin ${SPACE_DIR}

RUN chmod u+x ${SPACE_DIR}/satellite.exe

ARG STRIP_SPACE_BINARY=1

RUN if [ ${STRIP_SPACE_BINARY} -eq 1 ]; then \
        strip -s ${SPACE_DIR}/satellite.exe; \
    fi

COPY ./run_space.sh /run_space.sh

USER ${SPACE_USERNAME}

ENV VIRTUAL_ENV=${SPACE_DIR}/../fprime-venv

RUN python3 -m venv ${VIRTUAL_ENV}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade --no-cache-dir sympy 

ENTRYPOINT [ "bash", "/run_space.sh" ]

FROM ubuntu:18.04 as fprime-ground

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Etc/UTC

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get  install  -y \
        python3 \
        python3-pip \
        python3-venv \
        && apt-get clean autoclean \ 
        && rm -rf /var/lib/apt/lists/*

ARG GROUND_UID=1000
ARG GROUND_GID=1000
ARG GROUND_USERNAME=ground

ARG BUILD_USERNAME=has
ARG BUILD_EXE_DIR=/home/${BUILD_USERNAME}/fprime

ENV GROUND_DIR=/home/${GROUND_USERNAME}/ground-system

RUN if [ ${GROUND_UID:-0} -ne 0 ] && [ ${GROUND_GID:-0} -ne 0 ]; then \
    groupadd -g ${GROUND_GID} $GROUND_USERNAME &&\
    useradd -l -m -u ${GROUND_UID} -g $GROUND_USERNAME $GROUND_USERNAME; \
    fi 

RUN chmod -R o-rwx /home/${GROUND_USERNAME}

USER ${GROUND_USERNAME}

RUN mkdir -p ${GROUND_DIR}

WORKDIR ${GROUND_DIR}

ENV VIRTUAL_ENV=${GROUND_DIR}/fprime-venv

RUN python3 -m venv ${VIRTUAL_ENV}

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=fprime-builder ${BUILD_EXE_DIR}/fprime ${GROUND_DIR}/fprime

WORKDIR ${GROUND_DIR}/fprime/

RUN pip install --upgrade --no-cache-dir \
    wheel \
    setuptools \
    pip \ 
    sympy \
    fprime-tools \
    fprime-gds

COPY --from=fprime-builder ${BUILD_EXE_DIR}/QualsRef/build-artifacts/Linux/dict/RefTopologyAppDictionary.xml ${GROUND_DIR}/dict/RefTopologyAppDictionary.xml

USER ${GROUND_USERNAME}

COPY ./run_ground.sh /run_ground.sh

ENTRYPOINT [ "bash", "/run_ground.sh" ]