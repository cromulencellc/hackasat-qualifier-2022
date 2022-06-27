FROM ubuntu:focal
RUN apt-get update -qq && \
        apt-get install -y \
        build-essential less zsh clang \
        python3-dev python3-pip libffi-dev \
        virtualenvwrapper
RUN pip install angr
