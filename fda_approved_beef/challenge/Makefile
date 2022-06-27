TAG_BASE ?= has3/quals/fprime-exploitation
REGISTRY ?= registry.mlb.cromulence.com
STRIP_BINARY ?= 1

.PHONY: docker-build
docker-build:
	docker build --pull --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) fprime-challenge -t $(TAG_BASE)/challenge-builder:latest --target fprime-builder
	docker build --pull --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) fprime-challenge -t $(TAG_BASE)/challenge-space:latest --target fprime-space
	docker build --pull --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) fprime-challenge -t $(TAG_BASE)/challenge-ground:latest --target fprime-ground
	docker tag $(TAG_BASE)/challenge-builder:latest $(REGISTRY)/$(TAG_BASE)/challenge-builder:latest
	docker tag $(TAG_BASE)/challenge-space:latest $(REGISTRY)/$(TAG_BASE)/challenge-space:latest
	docker tag $(TAG_BASE)/challenge-ground:latest $(REGISTRY)/$(TAG_BASE)/challenge-ground:latest

.PHONY: docker-build-sysbox
docker-build-sysbox:
	cd /build/fprime-challenge && \
	docker build --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) . -t $(TAG_BASE)/challenge-builder:latest --target fprime-builder && \
	docker build --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) . -t $(TAG_BASE)/challenge-space:latest --target fprime-space && \
	docker build --build-arg STRIP_SPACE_BINARY=$(STRIP_BINARY) . -t $(TAG_BASE)/challenge-ground:latest --target fprime-ground && \
	docker tag $(TAG_BASE)/challenge-builder:latest $(REGISTRY)/$(TAG_BASE)/challenge-builder:latest && \
	docker tag $(TAG_BASE)/challenge-space:latest $(REGISTRY)/$(TAG_BASE)/challenge-space:latest && \
	docker tag $(TAG_BASE)/challenge-ground:latest $(REGISTRY)/$(TAG_BASE)/challenge-ground:latest && \
	cd /build

.PHONY: run-builder
run-builder:
	docker run -it --rm $(TAG_BASE)/challenge-builder:latest

.PHONY: run-system-local
run-system-local:
	docker-compose up -d --force-recreate

.PHONY: stop-system-local
stop-system-local:
	docker-compose logs -t > system-local.log
	docker-compose down
