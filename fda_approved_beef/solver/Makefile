TAG_BASE ?= has3/quals/fprime-exploitation
REGISTRY ?= registry.mlb.cromulence.com

.PHONY: build
build:
	docker build . -t $(TAG_BASE)/solver:latest
	docker tag $(TAG_BASE)/solver $(REGISTRY)/$(TAG_BASE)/solver:latest

.PHONY: run
run:
	docker run -it --rm \
	-e CHAL_HOST=172.16.238.3 \
	-e CHAL_PORT=5000 \
	--entrypoint=/bin/bash \
	$(REGISTRY)/$(TAG_BASE)/solver:latest "/home/ground/ground-system/solver.sh"