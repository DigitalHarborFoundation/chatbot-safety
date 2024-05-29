.PHONY: help install ensure-poetry install-precommits test run-streamlit build-docker run-docker remove-docker

export PATH := $(HOME)/.local/bin:$(PATH)

tt:
	@which poetry
	@poetry install

help:
	@echo "Relevant targets are 'install' and 'test'."

install:
	@$(MAKE) ensure-poetry
	@$(MAKE) install-precommits
	@poetry build
	@poetry run pip install --extra-index-url https://europe-west1-python.pkg.dev/rori-turn/rori-python-packages/simple/ rori-orm

ensure-poetry:
	@# see issue: https://stackoverflow.com/questions/77019756/make-not-finding-executable-added-to-path-in-makefile
	@if ! command -v poetry &> /dev/null; then \
		echo "Installing poetry"; \
		curl -sSL https://install.python-poetry.org | python - ; \
		echo "Poetry installed, but you might need to update your PATH before make will detect it."; \
	fi
	@poetry install

install-precommits:
	@poetry run pre-commit autoupdate
	@poetry run pre-commit install --overwrite --install-hooks

jupyter:
	poetry run jupyter lab

test:
	@poetry run pytest --cov=src --cov-report term-missing
