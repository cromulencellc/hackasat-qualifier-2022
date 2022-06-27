CHAL_NAME ?= power_level
CHAL_PORT ?= 10000
SAMPLE_PORT ?= 25000
CHAL_HOST ?= 172.17.0.1
#
PROD_URL  ?= satellitesabove.me
PROD_HOST ?= power_level.$(PROD_URL)
PROD_PORT ?= 5100
PROD_TICKET ?= ticket{kilo790094victor3:GMPdUI_1E8FkP4QRFlQG88RDo8SKGP8w5zgwXDTUl5-hftROMT1MZ0DPeXrxIG4aVw}


.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} -p ${SAMPLE_PORT}\:10001 ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"
	echo "Then connect with TCP on $(SAMPLE_PORT) for streaming samples"
.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} -e SERVICE_PORT=${SAMPLE_PORT} -p ${SAMPLE_PORT}\:10001 ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} -e SERVICE_PORT=${SAMPLE_PORT} ${CHAL_NAME}:solver
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver
push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
