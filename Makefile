### --------------------------------------------------------------------------------------------------------------------
### Variables
### (https://www.gnu.org/software/make/manual/html_node/Using-Variables.html#Using-Variables)
### --------------------------------------------------------------------------------------------------------------------

DC := docker compose
CLI := $(DC) run --rm cli

# Other config
NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m


### --------------------------------------------------------------------------------------------------------------------
### RULES
### (https://www.gnu.org/software/make/manual/html_node/Rule-Introduction.html#Rule-Introduction)
### --------------------------------------------------------------------------------------------------------------------
.PHONY: migration-script setup-database build run status logs stop down clean

migrate:
	$(DC) up -d app database
	@echo "revision name: "; \
	read MESSAGE; \
	$(DC) run --rm app sh -c "alembic revision -m '$$MESSAGE' --autogenerate"

setup-db:
	$(DC) run --rm app sh -c "alembic upgrade head"

build:
	$(DC) build

run:
	$(DC) up -d

status:
	$(DC) ps

logs:
	$(DC) logs -f

stop:
	$(DC) stop

down:
	$(DC) down

clean:
	$(DC) down -v --rmi local --remove-orphans

style:
	black .

test-unit:
	$(CLI) -m pytest -v --cov=./ --cov-report=xml --junitxml=pytests.xml app/tests