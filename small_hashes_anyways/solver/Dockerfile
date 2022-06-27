FROM registry.mlb.cromulence.com/has3/quals/microblaze-user-toolchain:bk-20220420 AS builder

RUN apk add ruby

RUN mkdir -p /solver

WORKDIR /solver

ADD solve.rb /solver

CMD ["/usr/bin/ruby", "/solver/solve.rb"]