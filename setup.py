#!/usr/bin/env python3

from pathlib import Path

from setuptools import setup

from ddt import __version__

root_dir = Path(__file__).parent
long_description = (root_dir / "README.md").read_text()

setup(
    name='ddt',
    description='Data-Driven/Decorated Tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Testing',
    ],
)
