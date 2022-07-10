COMPOSE = docker compose -f docker-compose.yml
ARGS = $(filter-out $@,$(MAKECMDGOALS))

help:
	@echo "shell             -- Open shell inside the container"
	@echo "check-imports     -- Check imports with isort"
	@echo "check-style       -- Check code-style"
	@echo "build             -- Rebuild the docker container"

shell:
	$(COMPOSE) run --rm mwc /bin/bash

test:
	$(COMPOSE) run --rm mwc pytest $(ARGS)

check-imports:
	$(COMPOSE) run --rm mwc isort **/*.py

check-style:
	$(COMPOSE) run --rm mwc black **/*.py

build:
	$(COMPOSE) build

stop:
	$(COMPOSE) down --remove-orphans

.PHONY: help bootstrap run shell test check-imports check-style build stop
