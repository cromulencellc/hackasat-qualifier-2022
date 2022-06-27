CHAL_NAME ?= basic_service
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1
SEED ?= 1465500232115169100
PROD_HOST ?= light-fever.95601890afd807.satellitesabove.me
TEST_PORT ?= 50030
PROD_PORT ?= 5030
DEMO_TICKET ?= ticket{quebec649483zulu2:GHkqSqZ5QULvyg2WIl6XnQ-s4oGG0wikfnw7q-Fbnb6u2ZohGBzoeDIZkWvVTziskg}

build: challenge solver



.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge

.PHONY:solver
solver: 
	docker build solver -t $(CHAL_NAME):solver

.PHONY:test
test:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} -e SEED=$(SEED) ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -it -e HOST=${CHAL_HOST} -e PORT=${CHAL_PORT} ${CHAL_NAME}:solver

.PHONY:test-aws
	docker run -it --rm -e "HOST=$(EC2_QA)" -e "PORT=$(6001)" -e "TICKET=ticket{zulu10571quebec:GKP9suZz2eyyEpgOpgn1fvN67EpR2MYxvtrAdVfdUtPjBA1w0QSGxD9cWz4grDWaOg}" $(CHAL_NAME):solver
	docker run -it --rm -e "HOST=$(EC2_QA)" -e "PORT=$(6001)" -e "TICKET=ticket{zulu49225delta:GOTiuy5qZHe9pz1v0x3r53PW_UNMDAxrgSDinuBHefq3TDMsX21k9G7Gn64pPdJEwA}" $(CHAL_NAME):solver

.PHONY:prod
prod:
	docker login registry.da39a3ee5e6b4b.satellitesabove.me:443
	docker pull registry.mlb.cromulence.com/has2/quals/challenges/basic-service/$(CHAL_NAME):challenge
	docker image tag registry.mlb.cromulence.com/has2/quals/challenges/basic-service/$(CHAL_NAME):challenge registry.da39a3ee5e6b4b.satellitesabove.me:443/$(CHAL_NAME):challenge
	docker push registry.da39a3ee5e6b4b.satellitesabove.me:443/$(CHAL_NAME):challenge

.PHONY:prod_test
prod_test:
	docker run -it -e HOST=${PROD_HOST} -e PORT=${PROD_PORT} -e "TICKET=$(DEMO_TICKET)" ${CHAL_NAME}:solver