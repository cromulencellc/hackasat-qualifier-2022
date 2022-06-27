CHAL_NAME ?= power_point
CHAL_PORT ?= 8000
SAMPLE_PORT ?= 8002
COMMAND_PORT ?= 8001
CHAL_HOST ?= 172.17.0.1

PROD_URL  ?= satellitesabove.me
PROD_HOST ?= power_point.$(PROD_URL)
PROD_PORT ?= 5100
PROD_TICKET ?= ticket{whiskey978242charlie3:GDLGD7Gg8Ut-te2ziOVEkuWMINSNd9lYIZQv_di1u1crRiSBsRl2YtFQcwjpJX3ALw}


.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(COMMAND_PORT)\:12001 -p $(SAMPLE_PORT)\:12002 -e SERVICE_PORT=${COMMAND_PORT} -e SERVICE_HOST=${CHAL_HOST} -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc $(CHAL_HOST) $(CHAL_PORT)"

.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(COMMAND_PORT)\:12001 -p $(SAMPLE_PORT)\:12002 -e SERVICE_PORT=${COMMAND_PORT}  -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver 
.PHONY:prod
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver 

push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
