CHAL_NAME ?= matters_of_state
CHAL_PORT ?= 8000
CHAL_HOST ?= 172.17.0.1
#
PROD_HOST ?= matters_of_state.test2022.satellitesabove.us
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{demo2tckt:GGzBql7g78poqcoxfCTOJ60rk-VsutivjdOdurV9Zw9W9XVuDA-P6tLk0nWCmbNuRg}

.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"
.PHONY:solver
solver:
	docker build challenge -t $(CHAL_NAME):challenge
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e SEED=1465500232115169100 -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -i -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver 
prod:
	docker build solver -t $(CHAL_NAME):solver
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e CHAL_TICKET=${PROD_TICKET} ${CHAL_NAME}:solver