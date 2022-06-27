CHAL_NAME ?= spiderverse
CHAL_PORT ?= 8000
CHAL_HOST ?= 172.17.0.1
CONFIG_PORT ?= 8001

PROD_URL  ?= satellitesabove.me
PROD_PORT ?= 5100
PROD_HOST ?= spiderverse.$(PROD_URL)
PROD_TICKET ?= ticket{romeo540664alpha3:GALbAdziTg_PiPzZTRHIJ_vNEvQzf2eJgqdhapvZMz9MmTrv1Bfutf3J9jXE701hXA}


.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(CONFIG_PORT)\:5000 -e SERVICE_PORT=$(CONFIG_PORT) -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"
	
.PHONY: generator
generator:
	docker build -t $(CHAL_NAME):generator -f ./generator/Dockerfile .
.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build -t $(CHAL_NAME):generator -f ./generator/Dockerfile .
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(CONFIG_PORT)\:5000 -e SERVICE_PORT=$(CONFIG_PORT)  -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run -v $(PWD)/data:/data $(CHAL_NAME):generator
	docker run --rm -i -v $(PWD)/data:/data -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} -e CONFIG_PORT:${CONFIG_PORT} ${CHAL_NAME}:solver 
.PHONY:
prod:
	docker build -t $(CHAL_NAME):generator -f ./generator/Dockerfile .
	docker build solver -t $(CHAL_NAME):solver
	docker run -v $(PWD)/data:/data $(CHAL_NAME):generator
	docker run --rm -i -v $(PWD)/data:/data -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver 


push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
