IN_DIR=requirements
DOCKER_DIR=docker

objects = $(wildcard $(IN_DIR)/*.in)
outputs = $(objects:.in=.txt)

.PHONY: requirements install-dev services run-dev

requirements: $(outputs)

# pip-tools
$(IN_DIR)/dev.txt: $(IN_DIR)/base.txt

%.txt: %.in ### Compile the requirements from the .in files
	pip-compile -v --output-file $@ $<

# dependencies
install-dev: ### Install development dependencies
	pip install -r $(IN_DIR)/dev.txt

# docker
services: ### Brings up the PostgreSQL database and the pgAdmin4
	docker-compose -p caption -f $(DOCKER_DIR)/docker-compose.services.yml up -d

# development:
run-dev: ### Runs the development server
	uvicorn main:app --reload

