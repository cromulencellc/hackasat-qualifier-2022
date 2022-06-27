CHAL_NAME ?= black_hole
CHAL_PORT ?= 31337
CHAL_HOST ?= 172.17.0.1
SERVICE_PORT ?= 19021

EC2_QA ?= ''
TICKET ?= '''
FLAG = flag{0bscur3!s3cur3}
TEST_HOST ?= black_hole.redteam.satellitesabove.us
TEST_PORT ?= 5300
PROD_HOST ?= black_hole.satellitesabove.me
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{india663163papa3:GLDCQYLAVdUKQB-IAryQDLSZWVHjshJEAFvoW_WUIBt-1a1GWwNhsIbHoq-xDx9Xow}
SEED ?= =4763612732172659022

DEMO_TICKET ?= ticket{demo8tckt:GFOi-HvfjOPP1tg4abM6HUPf7b1mN-GyVjmPhQsKjZvZDs4_Wn1jorjDu3r-U8-Q4w}

.PHONY:challenge solver all test
all: challenge solver test

challenge:
	docker build -f challenge/Dockerfile challenge -t ${CHAL_NAME}:challenge
solver:
	docker build -f solver/Dockerfile solver -t ${CHAL_NAME}:solver

test:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}\:solver


.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=${TEST_HOST} -e CHAL_PORT=${TEST_PORT} -e TICKET=$(DEMO_TICKET) ${CHAL_NAME}:solver


.PHONY:push-aws
push-aws:
	docker login registry.redteam.satellitesabove.us
	docker image tag $(CHAL_NAME):challenge registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge
	docker push registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge


.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge

.PHONY:test-prod
test-prod:
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=$(PROD_TICKET) ${CHAL_NAME}:solver

