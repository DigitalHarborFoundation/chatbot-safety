.PHONY: help install ensure-poetry install-precommits jupyter test

export PATH := $(HOME)/.local/bin:$(PATH)

help:
	@echo "Relevant targets are 'install' and 'test'."

install:
	@$(MAKE) ensure-poetry
	@$(MAKE) install-precommits

ensure-poetry:
	@# see issue: https://stackoverflow.com/questions/77019756/make-not-finding-executable-added-to-path-in-makefile
	@if ! command -v poetry &> /dev/null; then \
		echo "Installing poetry"; \
		curl -sSL https://install.python-poetry.org | python - ; \
		echo "Poetry installed, but you might need to update your PATH before make will detect it."; \
	fi
	@poetry install

install-precommits:
	@poetry run pre-commit install --overwrite --install-hooks

jupyter:
	poetry run jupyter lab

test:
	@poetry run pytest --cov=src --cov-report term-missing
