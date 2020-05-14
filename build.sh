#!/bin/bash
pytest --cov=ddt --cov-report html
flake8 ddt.py test || echo "Flake8 errors"
(cd docs; make html)
