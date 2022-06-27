CHAL_NAME ?= red_alert
CHAL_PORT ?= 3001
CHAL_HOST ?= 172.17.0.1
GRAFANA_PORT ?= 12000
build: generate challenge local solver

PROD_HOST ?= red_alert.satellitesabove.me
PROD_PORT ?= 5100
PROD_TICKET ?= ticket{kilo535174kilo3:GMah37_yL04OIPq-NFETWb-KXsmvOLXV7KWLkqaeZimTzNVc48qf4jqXtkzcOr_ieg}

# Local skips the out image "docker in docker" nature of the challenge
# This allows you to test things out easily before you go build all the DinD stuff
local:
	docker container prune
	cd challenge; sh start.sh

.PHONY:challenge
challenge:
	echo "Running challenge"
	docker build challenge -t $(CHAL_NAME):challenge
	docker run -d --runtime=sysbox-runc -p ${GRAFANA_PORT}:3000 -e SERVICE_PORT=${GRAFANA_PORT} -e SERVICE_HOST=${CHAL_HOST} red_alert:challenge > log 2>&1 &
	echo "This challenge takes a bit to come online...please wait 30 seconds"
	echo "Then to play: nc localhost $(CHAL_PORT)"

.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge

.PHONY:test-prod
test-prod:
	@echo $(PROD_TICKET)
	echo "$(PROD_TICKET)" | nc $(PROD_HOST) $(PROD_PORT)
