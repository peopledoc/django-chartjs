.PHONY: docs test clean

bin/python:
	virtualenv .
	bin/python setup.py develop

test: bin/python
	bin/pip install tox
	bin/tox

clean:
	rm -rf bin .tox include/ lib/ man/ django_chartjs.egg-info/ build/ demo/venv/

docs:
	(cd docs; make html)

.PHONY: demo
demo:
	test -d demo/venv || virtualenv demo/venv
	demo/venv/bin/pip install -e demo
	DJANGO_SETTINGS_MODULE=demoproject.settings demo/venv/bin/python demo/demoproject/manage.py runserver
