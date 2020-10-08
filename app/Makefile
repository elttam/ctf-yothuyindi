#!/usr/bin/make


.DEFAULT_GOAL := help

PYC_FILES := $(shell find . -type f -name '*.pyc')
FILES := $(PYC_FILES) .coverage
DIRS := htmlcov/ .pytest_cache/ tests/.pytest_cache/ tests/__pycache__/ yaml_to_json/__pycache__/

SECRET_KEY ?= test123

tests: test
test: _test htmlcov ## Run pytest with coverage

_test: venv requirements
	PYTHONPATH=. ../venv/bin/pytest -v --forked --cov

htmlcov: _test	## convert test coverage data to html report
	../venv/bin/coverage html

serve_cov: htmlcov ## Serve test coverage html report
	@echo "http://localhost:8000/"
	cd htmlcov && python3 -m http.server

clean: ## Delete non-source files like test coverage and cached files
	rm -rf $(DIRS)
	rm -f $(FILES)

ls_other: ## Display files not commited in git
	git ls-files --other

venv: ../venv/bin/activate ## Create python venv
../venv/bin/activate:
	test -d ../venv || python3 -m venv ../venv
	@echo "To activate venv, run: . ../venv/bin/activate"
	@echo "To deactivate venv, run: deactivate"

rm_venv: ../venv/ ## Remove python venv
	rm -rf ../venv/

wheel: ../venv/bin/wheel
../venv/bin/wheel:
	../venv/bin/pip install wheel

requirements: venv wheel requirements.txt	## Install python requirements in venv
	. ../venv/bin/activate && ../venv/bin/pip install -r requirements.txt

run:	requirements	## Run locally
	. ../venv/bin/activate && SECRET_KEY=$(SECRET_KEY) FLASK_APP=yaml_to_json flask run -p 8080

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: help test tests _test htmlcov clean ls_other rm_venv
