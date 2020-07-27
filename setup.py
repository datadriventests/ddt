#!/usr/bin/env python
# # coding: utf-8

from setuptools import setup
from ddt import __version__

setup(
    name='ddt',
    description='Data-Driven/Decorated Tests',
    long_description='A library to multiply test cases',
    version=__version__,
    author='Carles Barrobés',
    author_email='carles@barrobes.com',
    url='https://github.com/datadriventests/ddt',
    py_modules=['ddt'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
    ],
    setup_requires=['enum34; python_version < "3"'],
    install_requires=['enum34; python_version < "3"'],
)
