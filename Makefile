VENV_DIR = venv
PYTEST_COMMAND = "pytest --cov=ddt --cov-report html"
FLAKE8_COMMAND = "flake8 ddt.py test"
ISORT_COMMAND = "isort --check-only --diff --skip-glob=.tox ."

local_all: venv_test venv_flake8 venv_isort

all: test flake8 isort

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

.PHONY: test
test:
	sh -c $(PYTEST_COMMAND)

.PHONY: venv_test
venv_test: venv
	. venv/bin/activate; sh -c $(PYTEST_COMMAND)

.PHONY: flake8
flake8:
	sh -c $(FLAKE8_COMMAND)

venv_flake8: venv
	. venv/bin/activate; sh -c $(FLAKE8_COMMAND)

.PHONY: isort
isort:
	sh -c $(ISORT_COMMAND)

venv_isort: venv
	. venv/bin/activate; sh -c $(ISORT_COMMAND)

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean: clean-pyc
	rm -rf $(VENV_DIR) .noseids nosetests.xml .coverage
