# MAKEFLAGS=--no-builtin-rules --no-builtin-variables --always-make
# ROOT := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
# export PATH := $(ROOT)/scripts:$(PATH)

# gen_server:
# 	scripts/gen_server.sh

# migrate:
# 	scripts/migrate.sh

PHONY: lint
lint:
	@poetry run pre-commit run --all-files

PHONY: run_local
run_local:
	@poetry run uvicorn app.main:app --reload

PHONY: run_docker
run_docker:
	docker compose up --build
