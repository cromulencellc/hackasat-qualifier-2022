CHAL_NAME ?= starsabove
CHAL_PORT ?= 8000
CHAL_HOST ?= 172.17.0.1

PROD_PORT ?= 5500
PROD_HOST ?= starsabove.satellitesabove.me
PROD_TICKET ?= ticket{kilo882959bravo3:GHYCzg7glL1O8m_5m0z4t3GN7qVJ3CtKGpn87P6KyIfHwTw7AdtfHYkwUOHx_sXVPQ}

all: challenge generator solver

.PHONY:challenge
challenge:
	docker build -t $(CHAL_NAME):challenge -f docker/Dockerfile . --target=challenge

.PHONY: static
static:
	mkdir -p ./static
	docker build -t $(CHAL_NAME):static -f docker/Dockerfile . --target=generator
	docker run --rm -i --volume $(PWD)/static:/data ${CHAL_NAME}:static

.PHONY:solver
solver: 
	docker build solver -t $(CHAL_NAME):solver

.PHONY:test
test: challenge solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver 

.PHONY: prod 
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run -v $(PWD)/data:/data $(CHAL_NAME):static
	docker run --rm -i -v $(PWD)/data:/data -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=${PROD_TICKET} ${CHAL_NAME}:solver 

.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=$(PROD_HOST) -e CHAL_PORT=$(PROD_PORT) -e TICKET=$(PROD_TICKET) $(CHAL_NAME):solver

.PHONY:push-aws
push-aws: challenge
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge
