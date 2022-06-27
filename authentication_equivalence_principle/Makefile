CHAL_NAME ?= equivalence_principle
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1

PROD_TICKET ?= ticket{kilo508271sierra3:GE2-0d_78etGNAZmSEZwml1IvOy0hWl11PnKnmToJQipYclVt-oxblwvAOvtXIct5A}
PROD_HOST ?= equivalence_principle.satellitesabove.me
PROD_PORT ?= 5100

build: generator challenge solver

.PHONY: generator
generator:
	docker build generator -t ${CHAL_NAME}:generator
	docker run --rm -i --volume ${PWD}/data:/data ${CHAL_NAME}\:generator

	
.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	docker run -v $(PWD)/upload:/data $(CHAL_NAME):generator
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} $(CHAL_NAME)\:challenge" > log 2>&1 &
	echo "Connect with: nc localhost $(CHAL_PORT)"


.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build generator -t $(CHAL_NAME):generator
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} $(CHAL_NAME)\:challenge" > log 2>&1 &
	docker run -v $(PWD):/data $(CHAL_NAME):generator
	docker run --rm -i -v $(PWD):/data -e CHAL_HOST=$(CHAL_HOST) -e CHAL_PORT=$(CHAL_PORT) $(CHAL_NAME):solver

.PHONY: prod
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run -v $(PWD):/data $(CHAL_NAME):generator
	docker run --rm -i -v $(PWD):/data -e CHAL_HOST=$(PROD_HOST) -e CHAL_PORT=$(PROD_PORT) -e CHAL_TICKET=$(PROD_TICKET) $(CHAL_NAME):solver


.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge

.PHONY:test-prod
test-prod:
	docker run --rm -i -v $(PWD):/data -e CHAL_HOST=$(PROD_HOST) -e CHAL_PORT=$(PROD_PORT) -e CHAL_TICKET=$(PROD_TICKET) $(CHAL_NAME):solver
