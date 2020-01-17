VIRTUALENV = virtualenv --python python3
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
TOX = $(VENV)/bin/tox
DEV_STAMP = $(VENV)/.dev_env_installed.stamp
INSTALL_STAMP = $(VENV)/.install.stamp

.PHONY: docs test clean tox install-dev virtualenv
all: install

virtualenv: $(PYTHON)
$(PYTHON):
	$(VIRTUALENV) $(VENV)

tox: $(TOX)
$(TOX): virtualenv
	$(VENV)/bin/pip install tox

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) setup.py
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ue .
	touch $(INSTALL_STAMP)

install-dev: $(DEV_STAMP)
$(DEV_STAMP): $(INSTALL_STAMP)
	$(VENV)/bin/pip install -r test-requirements.pip
	$(VENV)/bin/pip install -e ./
	$(VENV)/bin/pip install -e demo/
	touch $(DEV_STAMP)

test: install-dev
	$(VENV)/bin/coverage run --branch --source=chartjs demo test demoproject

clean:
	rm -rf bin .tox include/ lib/ man/ django_chartjs.egg-info/ build/

docs:
	(cd docs; make html)

.PHONY: demo
demo: install-dev
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py runserver

demo-with-fixtures: install-dev
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py makemigrations demoproject
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py migrate
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py loaddata demo/demoproject/fixtures/meter-readings.json
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py runserver

demo-test: install-dev
	DJANGO_SETTINGS_MODULE=demoproject.settings $(PYTHON) demo/demoproject/manage.py test demoproject --verbose

.PHONY: black
black: install-dev
	$(VENV)/bin/black chartjs demo

.PHONY: isort
isort: install-dev
	$(VENV)/bin/isort -rc .isort.cfg chartjs demo
