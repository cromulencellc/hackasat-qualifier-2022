CHAL_NAME ?= doppler
FLAG ?= flag{zulu49225delta:GEuHu-lkVHZUryVLA926sLeEqnjP4C6ELc4fglSzpy92FOaFnGwcwWRB-Y_zDPijwJJzub-e5qr79IsIfgv3BiU}

.PHONY:generator
generator:
	docker build generator -t $(CHAL_NAME):generator
	rm -rf data/*
	docker run -i --rm -v $(PWD)/data:/out -e "FLAG=$(FLAG)" $(CHAL_NAME):generator

.PHONY:solver
solver: 
	docker build solver -t $(CHAL_NAME):solver
	docker run -it --rm -v $(PWD)/data:/data $(CHAL_NAME):solver