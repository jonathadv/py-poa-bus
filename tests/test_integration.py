# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention in the tests
# and because some entities are used seamlessly instead of being directly called.

# pylint: disable=invalid-name
# pylint: disable=unused-import


"""
tests.test_class_commands
------------------
The test set for functions in driloader.commands.Commands
"""


import pytest
import pytest_mock

from pypoabus import eptc_facade

class TestIntegration:
    """ Test Commands by mocking the subprocess calls """

    @staticmethod
    def test_get_real_south_zone_bus_list(mocker):
        """ """
        zone = 'south'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_north_zone_bus_list(mocker):
        """ """
        zone = 'north'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_east_zone_bus_list(mocker):
        """ """
        zone = 'east'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_public_zone_bus_list(mocker):
        """ """
        zone = 'public'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_south_zone_bus_timetable(mocker):
        """ """
        bus_line_code = '281-1'
        timetable = eptc_facade.get_bus_timetable(bus_line_code)

        assert timetable.code == bus_line_code.replace('-', '')
        assert timetable.name == 'CAMPO NOVO / MORRO AGUDO'
