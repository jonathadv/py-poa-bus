#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

""" CMD Helper Script """

import argparse
import sys
from collections import OrderedDict

from pypoabus import __version__
from . import pypoabus
from .exceptions import NoContentAvailableError, RemoteServerError


def _print_stderr(message, exit_cmd=False):
    """ Function print to stderr and close the cmd """
    print('pypoabus: %s' % message, file=sys.stderr)

    if exit_cmd:
        sys.exit(1)


def _print_stdout(message):
    """ Function to print to stdout """
    print(message, file=sys.stdout)


def get_table_line(data, index):
    """
    Function to retrieve each line from
    the table as a single string like:

    c1_value01    c2_value01

    The values are returnd inside a tuble.

    """
    result_array = []
    for key in data.keys():
        array = data[key]
        if len(array) > index:
            result_array.append(array[index])
        else:
            result_array.append('')
    return tuple(result_array)


def _build_table(title, data):
    """
        Function to build a table from
        a data structure as below:
        {
            'column1': ['c1_value1', 'c1_value2'],
            'column2': ['c2_value1', 'c2_value2']
        }

        It's basically a dict where each key
        represents a coloumn and each key's value
        must me a list of string that represents
        the coloumn's values.

    """
    columns_number = len(data.keys())
    max_column_length = 0

    for key in data.keys():
        column_length = len(data[key])

        if column_length > max_column_length:
            max_column_length = column_length

    line_template = '%s\t\t' * columns_number + '\n'

    table_string = '\n\t' * int(columns_number / 2) + title + '\n\n'
    table_string += line_template % tuple([key for key in data.keys()])
    table_string += '------------------------' * columns_number + '\n'

    for i in range(0, max_column_length):
        table_string += line_template % get_table_line(data, i)

    return table_string


def _list_to_json(list_of_obj):
    """ Convert a object list to a JSON list """
    output = '{ "list":  %s  }' % str(list_of_obj)
    _print_stdout(output)


def _run(args):
    """ Run it """

    output_format = args.format if args.format is not None else 'json'

    if args.debug_url:
        pypoabus.DEBUG_URLS = True

    try:
        if args.list is not None:
            lines_list = pypoabus.list_bus_lines(args.list)

            if output_format == 'table':
                line_names = [line.name for line in lines_list]
                line_codes = [line.code for line in lines_list]

                data = OrderedDict()
                data['Code'] = line_codes
                data['Name'] = line_names

                title = 'List of Bus lines'
                _build_table(title, data)

            else:
                _list_to_json(lines_list)

        elif args.timetable is not None:
            timetable = pypoabus.get_bus_timetable(args.timetable)

            if output_format == 'table':
                for sched in timetable.schedules:
                    data = OrderedDict()
                    data['Time'] = sched.timetable

                    title = '%s - %s | %s | %s' % (timetable.code,
                                                   timetable.name,
                                                   sched.schedule_day,
                                                   sched.direction)
                    table_string = _build_table(title, data)
                    _print_stdout(table_string)

            else:
                _print_stdout(timetable.to_json())

        else:
            _print_stderr('Error when parsing arguments: %s' % args, True)


    except NoContentAvailableError:
        _print_stderr('Unable to retrieve information from EPTC web site, '
                      'maybe the content is no longer available.\n', True)

    except RemoteServerError as excep:
        _print_stderr('Error to connect to the server: %s ' % excep, True)


def _get_opts():
    """ Function to parse the cmd arguments """

    parser = argparse.ArgumentParser(prog='pypoabus')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', required=False,
                       metavar='zone',
                       help='List all line codes by zone: [north|south|east|public]',
                       choices=['north', 'south', 'east', 'public'])

    group.add_argument('-t', '--timetable', required=False,
                       metavar='line_code',
                       help='Line code like 281-1 and 101-1')

    parser.add_argument('-f', '--format', metavar='format',
                        help='[json|table]',
                        required=False,
                        choices=['json', 'table'])

    parser.add_argument('-d', '--debug-url',
                        action='store_true',
                        help='Log the URL that pypoabus will call',
                        required=False)

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        return None

    return args


def main():
    """ Main function """
    args = _get_opts()
    if args:
        _run(args)

if __name__ == '__main__':
    main()
