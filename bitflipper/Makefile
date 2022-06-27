CHAL_NAME ?= bitflipper
CHAL_PORT ?= 31337
CHAL_HOST ?= 172.17.0.1
SERVICE_PORT ?= 19021

EC2_QA ?= ''
FLAG = flag{CONTACT_AN_ADMIN_IF_YOU_SEE_THIS}
PROD_HOST ?= ${CHAL_NAME}.satellitesabove.me
PROD_PORT ?= 5100
TICKET ?= ticket{india632154hotel3:GHoHGh6RDPJOb9m3GIT-DBK6wDYAYPkIqiKwKl2hnThG-S_t78BQVn4hLXpb1s7Z2g}
SEED ?= =4763612732172659022
PROD_TICKET ?= ""

.PHONY:challenge solver all test
all: challenge solver test

challenge:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge"
solve:
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}\:solver

static: build-static
	docker run -it --rm -v $(shell pwd)/static:/static ${CHAL_NAME}:static

build-static:
	docker build -f static/Dockerfile static -t ${CHAL_NAME}:static
build-challenge: static
	docker build -f challenge/sparc/Dockerfile . -t ${CHAL_NAME}:challenge
build-solver:
	docker build -f solver/sparc/Dockerfile solver -t ${CHAL_NAME}:solver

test: build-solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}\:solver


.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=${TICKET} ${CHAL_NAME}:solver


.PHONY:push-aws
push-aws: build-challenge
	docker login registry.satellitesabove.me
	docker image tag ${CHAL_NAME}:challenge registry.satellitesabove.me/${CHAL_NAME}:challenge
	docker push registry.satellitesabove.me/${CHAL_NAME}:challenge

