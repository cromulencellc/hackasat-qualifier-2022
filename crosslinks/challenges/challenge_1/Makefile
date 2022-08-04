CHAL_NAME ?= crosslinks
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1
#
PROD_URL  ?= satellitesabove.me
PROD_HOST ?= crosslinks.$(PROD_URL)
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{bravo484590zulu3:GBUrqMZZU0u_CLanGikC1sDU3vbWZJsrc6uMjKiceEiuI9rjR34hQgULcw7gCXCwow}
build: challenge solver

.PHONY:challenge
challenge:
	docker build -t crosslinks:base ../..
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &

.PHONY:solver
solver:
	docker build -t crosslinks:base ../../
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver
push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge