CHAL_NAME ?= its_a_wrap
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1
FLAG ?= flag{test123test123987654321qwertyuiopasdfghjkl1234567890}

TEST_HOST ?= its_a_wrap.redteam.satellitesabove.us
TEST_PORT ?= 5300
TICKET ?= ticket{demo2tckt:GIwSCf-I-5RI-lKEVqXFKmV9QEYBTiUdB0ADUL6evKFIeCBSzHhQQJTV4nrdmSKHWg}

PROD_HOST ?= its_a_wrap.satellitesabove.me
PROD_PORT ?= 5300
PROD_TICKET ?=  ticket{sierra327929lima3:GCOOdxiTpzBt-mU8yF3Q3QZa8usYfr1tB-v4fKv9F1K28oFUQdA21t_eDOdQaSCTsg} 

build: challenge solver static

.PHONY:challenge
challenge:
	docker build challenge --target=runner -t $(CHAL_NAME):challenge
	# docker run --rm -it --entrypoint=/bin/bash -e SEED=1465500232115169100 -e FLAG=$(FLAG) ${CHAL_NAME}\:challenge

.PHONY: generator
generator:
	mkdir -p ./static
	docker build  challenge --target=generator -t $(CHAL_NAME):generator
	docker run --rm -i --volume $(PWD)/static:/data ${CHAL_NAME}:generator
	
.PHONY:solver
solver: 
	docker build solver -t $(CHAL_NAME):solver

.PHONY:test
test:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=$(FLAG) ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver

.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=${TEST_HOST} -e CHAL_PORT=${TEST_PORT} -e TICKET=$(TICKET) ${CHAL_NAME}:solver


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

