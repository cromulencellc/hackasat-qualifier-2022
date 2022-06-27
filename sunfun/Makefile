CHAL_NAME ?= sunfun
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.20.0.1

PROD_HOST ?= sunfun.redteam.satellitesabove.us
PROD_PORT ?= 5300
TICKET ?= ticket{demo0tckt:GFAoajy0q4jYvPjlgbR7-f8-w3OnemTx8_s3J7A1R6XD_uRwH4kz9wM215DJKiIIJA}
FLAG ?= flag{zulu49225delta\:GG1EnNVMK3-hPvlNKAdEJxcujvp9WK4rEchuEdlDp3yv_Wh_uvB5ehGq-fyRowvwkWpdAMTKbidqhK4JhFsaz1k}

.PHONY:challenge
challenge:
	cp -rf static/* challenge/
	docker build challenge -t $(CHAL_NAME):challenge
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	echo "To connect: nc localhost $(CHAL_PORT)"

.PHONY:solver
solver:
	cp -rf static/* challenge/
	docker build challenge -t $(CHAL_NAME):challenge
	cp -rf static/* solver/
	docker build solver -t $(CHAL_NAME):solver
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -it -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver

.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=$(PROD_HOST) -e CHAL_PORT=$(PROD_PORT) -e TICKET=$(TICKET) ${CHAL_NAME}:solver


.PHONE:push-aws
push-aws:
	docker login registry.redteam.satellitesabove.us
	docker image tag $(CHAL_NAME):challenge registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge
	docker push registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge
