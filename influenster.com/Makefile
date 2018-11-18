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

define SPIDERKEEPR_DEPLOY_PYSCRIPT
import os
import sys
import configparser
from urllib.parse import urljoin

import requests
from scrapy.utils.conf import closest_scrapy_cfg

config = configparser.ConfigParser()
config.read(closest_scrapy_cfg())

project_name = config.get('deploy:spiderkeeper', 'project')
server_url = config.get('deploy:spiderkeeper', 'url')

response = requests.get(urljoin(server_url, '/api/projects'))
response.raise_for_status()
projects = response.json()

project_id = next(( each['project_id'] for each in projects if each['project_name'] == project_name), None)
if not project_id:
	response = requests.post(
		urljoin(server_url, '/api/projects'),
		data={'project_name': project_name}
	)
	response.raise_for_status()
	project_id = response.json()['project_id']

egg_file = next((each for each in os.listdir('dist') if each.endswith('.egg')), None)

response = requests.post(
	urljoin(server_url, "/project/%s/spider/upload" % project_id),
	files={'file': os.path.join('dist', egg_file)},
	headers={'Referer': server_url}
)
response.raise_for_status()
endef
export SPIDERKEEPR_DEPLOY_PYSCRIPT



help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc ## remove all build and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr *.egg-info
	rm -fr *.egg

clean-pyc: ## remove Python file artifacts
	find influenster -name '*.pyc' -exec rm -f {} +
	find influenster -name '*.pyo' -exec rm -f {} +
	find influenster -name '*~' -exec rm -f {} +
	find influenster -name '__pycache__' -exec rm -fr {} +

lint: ## lint code with pylint
	pipenv run pylint influenster

check: ## check installed dependencies for security vulnerabilities
	pipenv check

test: ## run spider contracts
	pipenv run scrapy check

dist: clean ## builds source, egg and wheel package
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_egg
	pipenv run python setup.py bdist_wheel
	ls -l dist

spiderkeeper-deploy: ## deploy project to spiderkeeper-deploy
	pipenv run python setup.py bdist_egg
	@pipenv run python -c "$$SPIDERKEEPR_DEPLOY_PYSCRIPT" "http://localhost:5000"

scrapyd-deploy: ## deploy project to scrapyd
	pipenv run scrapyd-deploy

deploy: spiderkeeper-deploy scrapyd-deploy ## deploy project to scrapyd and spiderkeeper

shell: ## spawn shell within the virtual environment
	pipenv shell

install: clean ## create virtual environment and install packages
	pip install pipenv --upgrade --user
	pipenv install --python 3.6 --dev

update: ## update installed packages in the virtual environment
	pipenv update

uninstall: clean ## purge all packages from virtual environment
	pipenv uninstall --all
