#!/bin/bash
nosetests --with-coverage --cover-html
flake8 ddt.py test || echo "Flake8 errors"
