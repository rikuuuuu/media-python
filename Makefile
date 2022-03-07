MAKEFLAGS=--no-builtin-rules --no-builtin-variables --always-make
ROOT := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
export PATH := $(ROOT)/scripts:$(PATH)

gen_server:
	scripts/gen_server.sh

migrate:
	scripts/migrate.sh

PHONY: lint
lint:
	@poetry run pre-commit run --all-files

PHONY: run_local
run_local:
	@poetry run uvicorn main:app --reload