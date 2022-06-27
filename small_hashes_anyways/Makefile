CHAL_NAME ?= small_hashes_anyways

.PHONY:generator
generator:
	docker build challenge -t $(CHAL_NAME):generator

.PHONY:solver
solver:
	docker build solver -t $(CHAL_NAME):solver

.PHONY: dev
dev:
	docker build -f Dockerfile-dev -t ominous-etude-dev .
	docker run --rm -it -v $(shell pwd):/mnt --security-opt seccomp=unconfined --cap-add SYS_PTRACE ominous-etude-dev

.PHONY: test
test:
	rm -rf tmp/test
	mkdir -p tmp/test
	docker run --rm -v $(PWD)/tmp/test:/out \
		-e "FLAG=flag{kilo73275yankee2:GLpXpjDWRQRmLDdyZwWmBiYKIbx4SkZp7u3Ak3WjpVy4RxI0luw2QwvLolmlmJm-vg}" \
		$(CHAL_NAME):generator
	docker run --rm -v $(PWD)/tmp/test:/mnt -e "BINARY_PATH=/mnt/small_hashes_anyways" \
		$(CHAL_NAME):solver
