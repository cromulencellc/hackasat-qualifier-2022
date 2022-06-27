#!/bin/sh

echo "Starting docker"
# dockerd start

dockerd  > ./log.txt 2>&1 &
sleep 10

cat ./log.txt
echo "Running build and pull"
# pull and build inner images
docker ps
make -f /build/Makefile docker-build-sysbox
# docker compose build
# docker compose pull

echo "Cleanup the container space"

echo "Cleanup docker"
# dockerd cleanup (remove the .pid file as otherwise it prevents
# dockerd from launching correctly inside sys container)
kill $(cat /var/run/docker.pid)
kill $(cat /run/docker/containerd/containerd.pid)
rm -f /var/run/docker.pid
rm -f /run/docker/containerd/containerd.pid
