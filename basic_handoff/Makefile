CHAL_NAME ?= basic_handoff
CHAL_PORT ?= 8000
CHAL_HOST ?= 172.17.0.1
#
PROD_URL ?= satellitesabove.me
PROD_HOST ?= basic_handoff.$(PROD_URL)
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{lima289031uniform3:GK2TFLCH25q59XER2exNdLdcrt8os69NMby1aHMKx4T1Tbx9o1G9IsfVog2hlEoljw}


.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -p 4000\:7100 -e SEED=1465500232115169100 -e SERVICE_PORT=4000 -e SERVICE_HOST=localhost -e FLAG=flag{TESTflag1234} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"

push_prod:
	docker tag $(CHAL_NAME):challenge registry.$(PROD_URL)/$(CHAL_NAME):challenge
	docker push registry.$(PROD_URL)/$(CHAL_NAME):challenge
.PHONY:prod
prod:
	nc $(PROD_HOST) $(PROD_PORT)
