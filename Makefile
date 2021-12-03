IN_DIR=requirements
DOCKER_DIR=docker

objects = $(wildcard $(IN_DIR)/*.in)
outputs = $(objects:.in=.txt)

.PHONY: requirements install-dev services

requirements: $(outputs)

# pip-tools
$(IN_DIR)/dev.txt: $(IN_DIR)/base.txt

%.txt: %.in
	pip-compile -v --output-file $@ $<

install-dev:
	pip install -r $(IN_DIR)/dev.txt

# docker
services:
	docker-compose -p caption -f $(DOCKER_DIR)/docker-compose.services.yml up -d

