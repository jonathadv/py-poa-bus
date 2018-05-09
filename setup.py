#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=no-name-in-module
# pylint: disable=import-error

"""
Setup Script
"""

from distutils.core import setup
from pypoabus import __version__, __author__, __author_email__, __license__

NAME = 'py-poa-bus'
DESCRIPTION = 'Application to retrieve the bus schedules of Porto Alegre city.'
REQUIRED = ['requests', 'beautifulsoup4']

setup(name=NAME,
      version=__version__,
      description=DESCRIPTION,
      author=__author__,
      author_email=__author_email__,
      license=__license__,
      packages=['pypoabus'],
      package_data={'pypoabus': ['config.json']},
      requires=REQUIRED,
     )
