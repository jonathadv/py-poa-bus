#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=invalid-name

"""
Setup Script
"""

from distutils.core import setup
from pypoabus import __version__, __author__, __author_email__, __license__
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt')
reqs = ['%s (%s%s)' % (ir.req.project_name,
                       ir.req.specs[0][0],
                       ir.req.specs[0][1]) for ir in install_reqs]

setup(name='PyPoABus',
      version=__version__,
      description='Application to retrieve the bus schedules of Porto Alegre city.',
      author=__author__,
      author_email=__author_email__,
      license=__license__,
      packages=['pypoabus'],
      package_data={'pypoabus': ['config.json']},
      requires=reqs,
     )
