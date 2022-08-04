CHAL_NAME ?= fly_me_to_the_moon
CHAL_PORT ?= 3000
CHAL_HOST ?= 172.17.0.1
SERVICE_PORT ?= 12000
PROD_URL ?= satellitesabove.me
PROD_TICKET ?= ticket{papa743616papa3:GM8ohruET3pyRv7thJSct6STBuabTKLygoVgUGPOiNUo7yVKyDEN6GCJLqwc60QRPg}

PROD_PORT ?= 5100
PROD_HOST ?= fly_me_to_the_moon.$(PROD_URL)

build: challenge solver

.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p ${SERVICE_PORT}\:8080 -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} -e SERVICE_PORT=${SERVICE_PORT} -e SERVICE_HOST=localhost ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "nc localhost $(CHAL_PORT) to play"
.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p ${SERVICE_PORT}\:8080 -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} -e SERVICE_PORT=${SERVICE_PORT} -e SERVICE_HOST=localhost ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver

prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver

push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge