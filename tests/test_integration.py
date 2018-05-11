# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention in the tests
# and because some entities are used seamlessly instead of being directly called.

# pylint: disable=invalid-name
# pylint: disable=unused-import


"""
tests.TestIntegration
------------------
The integration test set for functions in pypoabus.eptc_facade
"""


import pytest
import pytest_mock

from pypoabus import eptc_facade
from pypoabus.exceptions import RemoteServerError, NoContentAvailableError

class TestIntegration:
    """ Integration testing """

    @staticmethod
    def test_get_real_south_zone_bus_list():
        """ """
        zone = 'south'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_north_zone_bus_list():
        """ """
        zone = 'north'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_east_zone_bus_list():
        """ """
        zone = 'east'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_public_zone_bus_list():
        """ """
        zone = 'public'
        bus_list = eptc_facade.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert len(bus_list) > 0

    @staticmethod
    def test_get_real_south_zone_bus_timetable():
        """ """
        bus_line_code = '281-1'
        bus_line_name = 'CAMPO NOVO / MORRO AGUDO'
        timetable = eptc_facade.get_bus_timetable(bus_line_code)

        assert timetable.code == bus_line_code.replace('-', '')
        assert timetable.name == bus_line_name

    @staticmethod
    def test_error_when_sending_invalid_bus_line_code():
        """ """
        bus_line_code = 'foo'
        with pytest.raises(RemoteServerError, match=r'.*Unable to get EPTC page content.*'):
            eptc_facade.get_bus_timetable(bus_line_code)

    @staticmethod
    def test_error_when_html_does_not_contain_information(mocker):
        """ """
        mocker.patch('pypoabus.eptc_facade._get_html', return_value='<html></html>')

        bus_line_code = 'foo'
        with pytest.raises(NoContentAvailableError, match=r'.*Unable to retrieve information from EPTC web site.*'):
            eptc_facade.get_bus_timetable(bus_line_code)

