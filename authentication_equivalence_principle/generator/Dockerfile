FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

# Get all my apt dependencies
RUN apt-get update  -y \
&& apt-get upgrade -y \
&& apt-get install -y --no-install-recommends\
                   build-essential \
                   cmake
# Copy my stuff over
WORKDIR /generator

COPY *.cpp /generator/
COPY xxtea/ /generator/xxtea
COPY orbit_auth/ /generator/orbit_auth
COPY *.txt /generator/
COPY *.sh /generator/
# Make sure we do the build


VOLUME /data
# Create the binary 
RUN ls && \
    cmake -B build . && \
    cmake --build build

VOLUME /data

CMD ["sh", "run.sh"]
