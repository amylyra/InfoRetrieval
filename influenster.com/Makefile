.PHONY: clean clean-pyc clean-build help
.DEFAULT_GOAL := help


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
		match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
		if match:
				target, help = match.groups()
				print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT




help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc ## remove all build and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/ dist/ .eggs/ *.egg-info *.egg

clean-pyc: ## remove Python file artifacts
	find -name '*.py[co]' -exec rm -f {} +
	find -name '*~' -exec rm -f {} +
	find -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -rf .coverage .pytest_cache

lint: ## analyse code and report errors, potential problems, convention violations and complexity.
	pipenv run prospector

check-errors: ## analyse code and check for errors
	pipenv run pylint --errors-only makeupalley

check: ## check installed dependencies for security vulnerabilities
	pipenv check

contracts: ## run spider contracts
	pipenv run scrapy check --nolog

dist: clean check-errors ## builds source, egg and wheel package
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_egg
	pipenv run python setup.py bdist_wheel
	ls -l dist

scrapyd-deploy: ## deploy project to scrapyd
	pipenv run scrapyd-deploy

shell: ## spawn shell within the virtual environment
	pipenv shell

install: clean ## create virtual environment and install packages
	pipenv install --deploy --dev

update: ## update installed packages in the virtual environment
	pipenv update

uninstall: clean ## purge all packages from virtual environment
	pipenv uninstall --all
