CHAL_NAME ?= screaming_fist
CHAL_PORT ?= 5000
CHAL_HOST ?= 127.0.0.1
SERVICE_HOST ?= 127.0.0.1
SERVICE_PORT ?= 5001
FLAG ?= flag{ThisIsALongerTestFlagyMcFlagTehFLAG}

PROD_TICKET ?= ticket{romeo322474hotel3:GLO3rQx2Q3EPP4sheftBkGcc8qBjf7vMe_EXsGRuMCYXOpNz_zwxrjCfb23XiomcAw}
PROD_URL  ?= satellitesabove.me
PROD_HOST ?= screaming_fist.$(PROD_URL)
PROD_PORT ?= 5300

build: challenge solver

.PHONY: challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge

.PHONY: solver
solver:
	docker build solver -t $(CHAL_NAME):solver

.PHONY: test
test:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --net host --rm -i -e FLAG=$(FLAG) -e SERVICE_HOST=$(SERVICE_HOST) -e SERVICE_PORT=$(SERVICE_PORT) ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i --net host -e HOST=$(CHAL_HOST) -e PORT=$(CHAL_PORT) -e SERVICE_HOST=$(SERVICE_HOST) -e SERVICE_PORT=$(SERVICE_PORT) ${CHAL_NAME}\:solver

.PHONY: test_prod
test_prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e TICKET=$(PROD_TICKET) -e HOST=$(PROD_HOST) -e PORT=$(PROD_PORT) ${CHAL_NAME}\:solver

.PHONE:push_prod
push_prod:
	docker image tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge