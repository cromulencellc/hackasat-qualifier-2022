FROM alpine:3 

RUN apk add bash xz gawk python3 \
  alpine-sdk bison flex texinfo \
  qemu-microblaze 
ADD build_cross_gcc gcc-11.2.0.tar.gz binutils-2.38.tar.bz2 cloog-0.18.1.tar.gz glibc-2.35.tar.bz2 gmp-6.2.1.tar.bz2 isl-0.24.tar.bz2 linux-5.2.21.tar.gz mpc-1.2.1.tar.gz mpfr-4.1.0.tar.gz /opt
WORKDIR /opt
RUN ls
RUN ./build_cross_gcc