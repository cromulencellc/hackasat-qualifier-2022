CHAL_NAME ?= leggo
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1
FLAG ?= flag{aaaaaaaaaa}

PROD_URL  ?= satellitesabove.me
PROD_HOST ?= leggo.$(PROD_URL)
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{kilo797392lima3:GE29tY-FcZVTb_TWKN1TuMrR5O_iDDys7rNpMacILu8l-OfYQVIfJOkMj6W8LNE73Q}


build: challenge solver

.PHONY: challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run -i --rm --net host -e FLAG=$(FLAG)  $(CHAL_NAME)\:challenge" > log 2>&1 &

.PHONY: solver
solver:
	docker build solver -t $(CHAL_NAME):solver
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run -i --rm --net host -e FLAG=$(FLAG) $(CHAL_NAME)\:challenge" > log 2>&1 &
	docker run -it -v $(PWD)/images:/solver/images -e CHAL_HOST=$(CHAL_HOST) -e CHAL_PORT=$(CHAL_PORT) $(CHAL_NAME):solver

.PHONY: static
static:
	docker build static -t $(CHAL_NAME):static
	docker run -v $(PWD)/images:/data $(CHAL_NAME):static

.PHONY: test-aws
test-aws:
	docker build solver -t $(CHAL_NAME):solver
	docker run -it -v $(PWD)/images:/solver/images -e TICKET=$(PROD_TICKET) -e CHAL_HOST=$(PROD_HOST) -e CHAL_PORT=$(PROD_PORT) $(CHAL_NAME):solver

push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
