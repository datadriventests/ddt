VENV_DIR = venv
FLAKE8_COMMAND = "flake8 ddt.py test"

local_all: venv_test venv_flake8 venv_isort

all: test flake8

install:
	python setup.py install
	pip install -Ur requirements.txt

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

.PHONY: test
test: install
	sh -c pytest

.PHONY: venv_test
venv_test: venv
	. venv/bin/activate; sh -c pytest

.PHONY: flake8
flake8: install
	sh -c $(FLAKE8_COMMAND)

.PHONY: venv_flake8
venv_flake8: venv
	. venv/bin/activate; sh -c $(FLAKE8_COMMAND)

.PHONY: venv_isort
venv_isort: venv
	. venv/bin/activate; sh -c $(ISORT_COMMAND)

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean: clean-pyc
	rm -rf $(VENV_DIR) .noseids nosetests.xml .coverage
