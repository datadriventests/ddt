#!/bin/bash
nosetests --with-coverage --cover-html --cover-package=ddt
flake8 ddt.py test || echo "Flake8 errors"
(cd docs; make html)
