# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Disabling the below pylint warnings in order to use long names convention in the tests
# and because some entities are used seamlessly instead of being directly called.

# pylint: disable=invalid-name
# pylint: disable=unused-import


"""
tests.TestIntegration
------------------
The integration test set for functions in pypoabus.__main__
"""

import pytest
import pytest_mock
import requests

from pypoabus import __main__, __title__, __version__
from pypoabus.pypoabus import BusLine


def test_get_version(mock, capsys):
    """ Check if -v returns the correct application version """
    mock.patch('sys.argv', ['', '-v'])
    expected = '{} {}\n'.format(__title__, __version__)
    try:
        __main__.main()
    except SystemExit:
        pass

    capture_result = capsys.readouterr()
    assert capture_result.out == expected


def test_get_line_list_from_valid_zone(mock, capsys):
    """ Checks if cli returns the correct bus list in unformatted json
     for correct zone
     """
    expected = '{ "list":  ["l1", "l2"] }\n'
    mock.patch('sys.argv', ['', '-l', 'south'])
    mock.patch('pypoabus.pypoabus.list_bus_lines', return_value='["l1", "l2"]')

    try:
        __main__.main()
    except SystemExit:
        pass

    capture_result = capsys.readouterr()
    assert capture_result.out == expected


def test_get_line_list_from_invalid_zone(mock, capsys):
    """ Checks if cli returns the correct error message
    for incorrect zone argument
    """
    zone = 'NOT_VALID_ZONE'
    mock.patch('sys.argv', ['', '-l', zone])
    expected = "usage: {} [-h] [-v] [-l zone | -t line_code] [-f format]" \
               " [-d]\npypoabus: error: argument -l/--list: " \
               "invalid choice: '{}' (choose from 'north', " \
               "'south', 'east', 'public')\n".format(__title__, zone)

    try:
        __main__.main()
    except SystemExit:
        pass

    capture_result = capsys.readouterr()
    assert capture_result.err == expected


def test_get_timetable_from_valid_line(mock, capsys):
    """ Checks if cli returns the correct bus timetable in unformatted json
    for the correct busline
    """
    expected = '{"code": "bar", "name": "foo", "schedules": []}\n'
    mock.patch('sys.argv', ['', '-t', 'non_existing_line'])
    mock.patch('pypoabus.pypoabus.get_bus_timetable', return_value=BusLine('foo', 'bar'))

    try:
        __main__.main()
    except SystemExit:
        pass

    capture_result = capsys.readouterr()
    assert capture_result.out == expected


def test_get_timetable_from_invalid_line(mock, capsys):
    """ Checks if cli returns the correct error message
    for the incorrect busline argument
    """
    expected = 'pypoabus: Error to connect to the server: ' \
                      'Unable to get EPTC page content. HTTP code: 500, reason: ' \
                      'Internal Server Error\n\n'

    mocked_response = requests.Response()
    mocked_response.status_code = 500
    mocked_response.reason = 'Internal Server Error'
    mock.patch('sys.argv', ['', '-t', 'non_existing_line'])
    mock.patch('requests.get', return_value=mocked_response)

    try:
        __main__.main()
    except SystemExit:
        pass

    capture_result = capsys.readouterr()
    assert capture_result.err == expected
