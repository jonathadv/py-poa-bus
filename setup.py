#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=no-name-in-module
# pylint: disable=import-error

"""
Setup Script
"""

from setuptools import setup
from pypoabus import __name__, __version__, __author__, __author_email__, __license__

with open("README.md", "r") as fh:
    long_description = fh.read()

DESCRIPTION = 'Module/CLI to retrieve the bus timetables of Porto Alegre city from EPTC web site.'
REQUIRED = ['requests', 'beautifulsoup4']

setup(name=__name__,
      version=__version__,
      description=DESCRIPTION,
      author=__author__,
      author_email=__author_email__,
      license=__license__,
      packages=['pypoabus'],
      package_data={'pypoabus': ['config.json']},
      requires=REQUIRED,
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic:: Utilities'
      ]
     )
