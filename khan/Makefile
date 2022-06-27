CHAL_NAME ?= khan
CHAL_PORT ?= 3000
CHAL_HOST ?= 172.17.0.1
SERVICE_PORT ?= 4000
FLAG ?= flag{TestFlagTheFlag}

TEST_HOST ?= khan.redteam.satellitesabove.us 
TEST_PORT ?= 5300
TEST_TICKET ?= ticket{demo9432ticket:GKTy8AwLrKXona3jrkU5v2LfpCavCV60zgWfCBvpTQr7m8Q6bVq4cik1xvVZ03iigw}

PROD_HOST ?= khan.satellitesabove.me
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{lima850736uniform3:GOPq2j42KRHhjgpWQgQv1CqDI_4s8OfRZcuT5FApgrVPkTUci2Mt1OFDrdiaiJoJzQ}


.PHONY: challenge
challenge:
	docker build -t $(CHAL_NAME):challenge challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(SERVICE_PORT)\:7100 -e SERVICE_PORT=$(SERVICE_PORT) -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"
.PHONY: static
static:
	docker build -t $(CHAL_NAME):static static 
	docker run -v $(PWD):/home/builder/data/ $(CHAL_NAME):static

.PHONY: solver
solver:
	docker build -t $(CHAL_NAME):static static
	docker build -t $(CHAL_NAME):challenge challenge
	docker build -t $(CHAL_NAME):solver solver
	docker run -v $(PWD):/home/builder/data/ $(CHAL_NAME):static
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p $(SERVICE_PORT)\:7100 -e SERVICE_HOST=$(CHAL_HOST) -e SERVICE_PORT=$(SERVICE_PORT) -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run -it -e CHAL_PORT=$(CHAL_PORT) -e CHAL_HOST=$(CHAL_HOST) -v $(PWD):/data $(CHAL_NAME):solver

.PHONY: test-aws
test-aws:
	docker build -t $(CHAL_NAME):static static
	docker build -t $(CHAL_NAME):solver solver
	docker run -v $(PWD):/home/builder/data/ $(CHAL_NAME):static
	docker run -it -e CHAL_PORT=$(TEST_PORT) -e CHAL_HOST=$(TEST_HOST) -e TICKET=$(TEST_TICKET) -v $(PWD):/data $(CHAL_NAME):solver

.PHONY: test-prod
test-prod:
	docker build -t $(CHAL_NAME):static static
	docker build -t $(CHAL_NAME):solver solver
	docker run -v $(PWD):/home/builder/data/ $(CHAL_NAME):static
	docker run -it -e CHAL_PORT=$(PROD_PORT) -e CHAL_HOST=$(PROD_HOST) -e TICKET=$(PROD_TICKET) -v $(PWD):/data $(CHAL_NAME):solver

.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge

	