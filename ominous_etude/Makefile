CHAL_NAME ?= ominous_etude
CHAL_PORT ?= 1975
CHAL_HOST ?= 172.17.0.1

TICKET ?= ticket{oscar880988delta3:GEiBCaiPgtk7_zVwX651b-uWrto3DXhxM8auUqZyIHAzjWbQlTZmK0IdIXdC08qY_g}

PROD_URL  ?= satellitesabove.me
PROD_HOST ?= ominous_etude.$(PROD_URL)
PROD_PORT ?= 5300

.PHONY:challenge

challenge:
	docker build runner -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"

.PHONY:solver
solver:
	# docker build runner -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver
.PHONY: dev
dev:
	docker build -f Dockerfile-dev -t ominous-etude-dev .
	docker run --rm -it -v $(shell pwd):/mnt --security-opt seccomp=unconfined --cap-add SYS_PTRACE ominous-etude-dev

.PHONY: embedded
embedded:
	docker build challenge -t $(CHAL_NAME):embedded
	docker run --rm -it -v $(shell pwd)/runner:/data $(CHAL_NAME):embedded

.PHONY: prod
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e TICKET=${TICKET} -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} ${CHAL_NAME}:solver



.PHONE:push_prod
push_prod:
	docker image tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
