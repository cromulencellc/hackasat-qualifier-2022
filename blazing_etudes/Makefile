CHAL_NAME ?= blazin_etudes
CHAL_PORT ?= 5000
CHAL_HOST ?= 172.17.0.1
PROD_URL  ?= satellitesabove.me
PROD_HOST ?= blazin_etudes.$(PROD_URL)
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{lima154577uniform3:GEpXCTzo28eHpI_1BRo0ywmjBZ6LJMe_4R5zYUIUuj53TIIym8gDRXsbTGfzXhhQfA}


.PHONY:challenge
challenge:
	docker build runner -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"

.PHONY:solver
solver:
	docker build runner -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver

.PHONY:builder
builder:
	docker build challenge -t $(CHAL_NAME):builder

.PHONY: dev
dev:
	docker build -f Dockerfile-dev -t ominous-etude-dev .
	docker run --rm -it -v $(shell pwd):/mnt --security-opt seccomp=unconfined --cap-add SYS_PTRACE ominous-etude-dev


prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=${PROD_TICKET} ${CHAL_NAME}:solver
push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
