# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention in the tests
# and because some entities are used seamlessly instead of being directly called.

# pylint: disable=invalid-name
# pylint: disable=unused-import


"""
tests.TestIntegration
------------------
The integration test set for functions in pypoabus.pypoabus
"""


import pytest
import pytest_mock

from pypoabus import pypoabus
from pypoabus.exceptions import NoContentAvailableError, RemoteServerError


class TestIntegration:
    """ Integration testing """

    @staticmethod
    def test_get_real_south_zone_bus_list():
        """ Get the south zone bus list from EPTC website """
        zone = 'south'
        bus_list = pypoabus.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert bus_list

    @staticmethod
    def test_get_real_north_zone_bus_list():
        """ Get the north zone bus list from EPTC website """
        zone = 'north'
        bus_list = pypoabus.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert bus_list

    @staticmethod
    def test_get_real_east_zone_bus_list():
        """ Get the east zone bus list from EPTC website """
        zone = 'east'
        bus_list = pypoabus.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert bus_list

    @staticmethod
    def test_get_real_public_zone_bus_list():
        """ Get the public bus list from EPTC website """
        zone = 'public'
        bus_list = pypoabus.list_bus_lines(zone)

        assert isinstance(bus_list, list)
        assert bus_list

    @staticmethod
    def test_get_real_south_zone_bus_timetable():
        """ Get a south zone bus timetble from EPTC website """
        bus_line_code = '281-1'
        bus_line_name = 'CAMPO NOVO / MORRO AGUDO'
        timetable = pypoabus.get_bus_timetable(bus_line_code)

        assert timetable.code == bus_line_code.replace('-', '')
        assert timetable.name == bus_line_name

    @staticmethod
    def test_error_when_sending_invalid_bus_line_code():
        """ Check if correct error is raised when trying to fetch invalid bus line code """
        bus_line_code = 'foo'
        with pytest.raises(RemoteServerError, match=r'.*Unable to '
                                                    r'get EPTC page content.*'):
            pypoabus.get_bus_timetable(bus_line_code)

    @staticmethod
    def test_error_when_html_does_not_contain_information(mocker):
        """ Check if correct error is raised when the response HTML does not contain information """
        mocker.patch('pypoabus.pypoabus._get_html', return_value='<html></html>')

        bus_line_code = 'foo'
        with pytest.raises(NoContentAvailableError, match=r'.*Unable to retrieve '
                                                          r'information from EPTC web site.*'):
            pypoabus.get_bus_timetable(bus_line_code)
