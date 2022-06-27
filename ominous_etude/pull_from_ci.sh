#!/bin/sh

docker pull registry.mlb.cromulence.com/has3/quals/challenges/ominous_etude:challenge
docker pull registry.mlb.cromulence.com/has3/quals/challenges/ominous_etude:solver

docker tag registry.mlb.cromulence.com/has3/quals/challenges/ominous_etude:challenge ominous_etude:challenge
docker tag registry.mlb.cromulence.com/has3/quals/challenges/ominous_etude:solver ominous_etude:solver