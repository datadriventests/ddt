VENV_DIR = venv

venv:
	$(shell virtualenv $(VENV_DIR))

test-env: | venv
	( \
		source $(VENV_DIR)/bin/activate; \
		pip install -r requirements/test.txt; \
	)

test: test-env
	( \
		source $(VENV_DIR)/bin/activate; \
		nosetests --with-coverage --cover-html --cover-package=ddt; \
	)

clean:
	rm -rf $(VENV_DIR) .noseids nosetests.xml .coverage
