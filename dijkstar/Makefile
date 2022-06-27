CHAL_NAME ?= once_unop_a_dijkstar
CHAL_PORT ?= 12345
CHAL_HOST ?= 172.17.0.1
TICKET ?= ticket{zulu10571quebec:GKP9suZz2eyyEpgOpgn1fvN67EpR2MYxvtrAdVfdUtPjBA1w0QSGxD9cWz4grDWaOg}
FLAG ?= flag{zulu49225delta\:GG1EnNVMK3-hPvlNKAdEJxcujvp9WK4rEchuEdlDp3yv_Wh_uvB5ehGq-fyRowvwkWpdAMTKbidqhK4JhFsaz1k}

TEST_HOST ?= once_unop_a_dijkstar.redteam.satellitesabove.us
TEST_PORT ?= 5300
TEST_TICKET ?= ticket{demo7tckt:GM_kurgZVoi35l6I8Lk_z87Wx5qV_YwC__a2shvDC8V4RrLpSg1r9vl47pq1swtVEA}

PROD_HOST ?= once_unop_a_dijkstar.satellitesabove.me
PROD_PORT ?= 5300
PROD_TICKET ?= ticket{uniform392890zulu3:GMYmgVCO8YG1o-E1NLGmBXdxdLRKeJ9qLQqx8QmdMOS8PgcY8TPOgB-e9CTQ47CUCg}

build: challenge solver

.PHONY:challenge
challenge:
	docker build challenge -t $(CHAL_NAME):challenge

.PHONY:solver
solver: 
	docker build solver -t $(CHAL_NAME):solver

.PHONY:test
test:
	socat -v tcp-listen:$(CHAL_PORT),reuseaddr exec:"docker run --rm -i -e FLAG=${FLAG} ${CHAL_NAME}\:challenge" > log 2>&1 &
	docker run --rm -it -e CHAL_HOST=${CHAL_HOST} -e CHAL_PORT=${CHAL_PORT} ${CHAL_NAME}:solver

.PHONY:test-aws
test-aws:
	docker run --rm -i -e CHAL_HOST=${TEST_HOST} -e CHAL_PORT=${TEST_PORT} -e TICKET=$(TEST_TICKET) ${CHAL_NAME}:solver


.PHONY:push-aws
push-aws:
	docker login registry.redteam.satellitesabove.us
	docker image tag $(CHAL_NAME):challenge registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge
	docker push registry.redteam.satellitesabove.us/$(CHAL_NAME):challenge

.PHONY:test-prod
test-prod:
	docker run --rm -i -e CHAL_HOST=${PROD_HOST} -e CHAL_PORT=${PROD_PORT} -e TICKET=$(PROD_TICKET) ${CHAL_NAME}:solver

.PHONY:push-prod
push-prod:
	docker login registry.satellitesabove.me
	docker image tag $(CHAL_NAME):challenge registry.satellitesabove.me/$(CHAL_NAME):challenge
	docker push registry.satellitesabove.me/$(CHAL_NAME):challenge