REPO_NAME ?= fprime-exploitation
CHAL_NAME ?= fda_approved_beef
CHAL_PORT ?= 1234
WEB_PORT ?= 12345
CLI_PORT ?= 12346
CHAL_PORT2 ?= 12346
# CHAL_HOST ?= 172.20.0.2
CHAL_HOST ?= 127.0.0.1
GROUND_HOST ?= 172.16.238.3
FLAG ?= flag{test123test123987654321qwertyuiopasdfghjkl1234567890}
CHAL_TIMEOUT ?= 900
TEST_TIMEOUT ?= 120

PROD_HOST ?= fda_approved_beef.satellitesabove.me
PROD_PORT ?= 5500
PROD_TICKET ?= ticket{alpha735639xray3:GNGQyAYUvCt8sh9Eh3IpuVPXITcbzPLoy9mw3C6ppahEwyp-9t13wQ2W8SzgevZS6A}

STRIP_BINARY ?= 1

TEST_HOST ?= fprime_exploitation.redteam.satellitesabove.us
TEST_PORT ?= 5500
TEST_TICKET ?= ticket{demo8tckt:GBuK60VTyOZYBpqD6F-Z6U6hzmWzVrNrJoWdTsgQY8xxY01w05Si3sax2pfktrC5_w}

build: challenge solver
build-local: challenge-local solver
EC2_QA ?= ec2-3-19-242-205.us-east-2.compute.amazonaws.com
TICKET ?= ticket{zulu10571quebec:GKP9suZz2eyyEpgOpgn1fvN67EpR2MYxvtrAdVfdUtPjBA1w0QSGxD9cWz4grDWaOg}

.PHONY:challenge
challenge:
	docker build --no-cache --pull challenge -t $(CHAL_NAME):challenge
	docker tag $(CHAL_NAME):challenge registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):challenge

.PHONY:challenge-local
challenge-local:
	$(MAKE) -C challenge docker-build

.PHONY:solver
solver: challenge-local
	docker build solver -t $(CHAL_NAME):solver
	docker tag $(CHAL_NAME):solver registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):solver

.PHONY:test
test:
	./test-sysbox.sh $(CHAL_HOST) $(CHAL_PORT) $(WEB_PORT) $(CLI_PORT) $(FLAG) $(TEST_TIMEOUT)
	
.PHONY:test-local
test-local:
	$(MAKE) -C challenge run-system-local
	docker run --network="challenge_fprime_net" -e CHAL_HOST=$(GROUND_HOST) registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):solver
	$(MAKE) -C challenge stop-system-local


.PHONY:solver-shell
solver-shell:
	docker run --rm -it --network="challenge_fprime_net" --entrypoint=/bin/bash -e CHAL_HOST=$(GROUND_HOST) registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):solver

.PHONY:test-aws
test-aws:
	docker run -it --rm -e "CHAL_HOST=$(TEST_HOST)" -e "CHAL_PORT=$(TEST_PORT)" -e "TICKET=$(TEST_TICKET)" registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):solver

.PHONY:push-aws
push-aws:
	docker login registry.redteam.satellitesabove.us
	# docker pull registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):challenge
	docker image tag registry.mlb.cromulence.com/has3/quals/challenges/$(REPO_NAME)/$(CHAL_NAME):challenge registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge



.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge

.PHONY:test-prod
test-prod:
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=$(PROD_TICKET) ${CHAL_NAME}:solver
