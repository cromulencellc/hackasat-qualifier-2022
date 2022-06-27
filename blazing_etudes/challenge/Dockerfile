FROM registry.mlb.cromulence.com/has3/quals/microblaze-user-toolchain:bk-20220420 AS builder

RUN apk add ruby

RUN mkdir -p /challenge/src /challenge/build

WORKDIR /challenge

ADD Makefile generate.rb /challenge/
ADD src /challenge/src
