#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='reqon',
    version='0.1.0',
    author='Derek Payton',
    author_email='derek.payton@gmail.com',
    description='A basic JSON to ReQL query builder.',
    keywords='rethinkdb',
    license='MIT',
    url='https://github.com/dmpayton/reqon',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    install_requires=['geojson', 'rethinkdb', 'six'],
)
