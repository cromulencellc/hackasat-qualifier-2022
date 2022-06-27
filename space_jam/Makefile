CHAL_NAME ?= space_jam
CHAL_PORT ?= 8000
SAMPLE_PORT ?= 8001
CHAL_HOST ?= 172.17.0.1
TEST_FLAG ?= flag{AReallyReallyReallyReallyReallyReallyLongAFflagForYouDawg}

PROD_TICKET ?= ticket{papa196606lima3:GG1x3K8R7rTx4bKTCa-SdwIkKn99ISOxYQwVV-GUo-98wnVGyO0FsEXv3I5pW-hImg}
PROD_URL  ?= satellitesabove.me
PROD_HOST ?= space_jam.$(PROD_URL)
PROD_PORT ?= 5300 
.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(SAMPLE_PORT)\:12001 -e SERVICE_PORT=$(SAMPLE_PORT) -e SEED=1465500232115169100 -e FLAG=${TEST_FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc $(CHAL_HOST) $(CHAL_PORT)"
	echo "Then connect via TCP at $(SAMPLE_PORT) for samples"
.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SERVICE_PORT=$(SAMPLE_PORT) -p $(SAMPLE_PORT)\:12001 -e SEED=1465500232115169100 -e FLAG=${TEST_FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver 

.PHONY:prod
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver

.PHONY:push_prod
push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
