# Contributing to DDT

We'll be happy if you want to contribute to the improvement of `ddt`.

Code contributions will take the form of pull requests to
[the github repo](https://github.com/txels/ddt).

Your PRs are more likely to be merged quickly if:

 - They adhere to coding conventions in the repo (PEP8)
 - They include tests

## Building


The simplest way to build `ddt` is using `tox`:

```
pip install tox
tox
```

This will run tests on various releases of python (2 and 3, as long as they
are installed in your computer), run `flake8` and build the Sphinx
documentation.

PRs to `ddt` are always built by travis-ci using tox.

Alternatively, if you ony want to run tests on your active version of python,
I recommend you make yourself a virtual environment and:

```
pip install -r requirements/build.txt
./build.sh
```
