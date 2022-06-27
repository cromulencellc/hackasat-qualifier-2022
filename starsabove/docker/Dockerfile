FROM rust:buster AS builder

WORKDIR /src
RUN cargo search --limit=0

COPY Cargo.toml /src/
COPY client /src/client
COPY messages /src/messages
COPY routelib /src/routelib
COPY server /src/server
COPY tests /src/tests

RUN cargo build --release --bin=client
RUN cargo build --release --bin=server

FROM debian:bullseye AS generator
WORKDIR /generator
COPY --from=builder /src/target/release/client /generator/challenge
COPY docker/generator.sh /generator
VOLUME /data
CMD ["sh", "/generator/generator.sh"]

FROM debian:bullseye AS challenge

RUN apt update -q -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y -q --no-install-recommends \
        gosu && \
    apt clean

WORKDIR /src
COPY --from=builder /src/target/release/client /src/client
COPY --from=builder /src/target/release/server /src/server
COPY docker/entrypoint.sh /

RUN chmod 0700 /entrypoint.sh && \
    chmod 0550 /src/* && \
    groupadd -r client && \
    groupadd -r server && \
    useradd -r -s /bin/false -g client client && \
    useradd -r -s /bin/false -g server client2 && \
    useradd -r -s /bin/false -g server client8 && \
    useradd -r -s /bin/false -g server server && \
    chown client:server /src/client && \
    chown server:server /src/server 

ENTRYPOINT ["/entrypoint.sh"]
