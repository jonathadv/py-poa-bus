#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

""" CMD Helper Script """

import argparse
import itertools
import sys

from pypoabus import __title__, __version__
from terminaltables import SingleTable

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


def _build_timetable_as_table(bus_line):
    """ This function first divides the bus schedules by its direction like
    Neighborhood -> Downtown or Downtown -> Neighborhood, in portuguese
    "BAIRRO/CENTRO" and "CENTRO/BAIRRO".
    Once, divided, it's created a table for direction using  `terminaltables`,
    where the column header value is the `schedule_day` property.

    The spected output is a string like:

    ┌BAIRRO/CENTRO─────────┬──────────┐  <-- The direction
    │ Dias Úteis │ Sábados │ Domingos │  <-- The schedule_day property
    ├────────────┼─────────┼──────────┤
    │ 05:30      │ 06:00   │ 06:30    │  <-- Timetable values
    │ 05:54      │ 06:15   │ 07:03    │

    """
    direction_dict = {}

    output_title = SingleTable([['   {} - {}  '.format(bus_line.code, bus_line.name)]])
    output = '{}\n'.format(output_title.table)
    header_blank_spaces = ' '

    # Checks if the table has enough width to carry the title, otherwise, adds more spaces
    # to the columns' headers in order to increase the table width.
    # Usually the table is not big enough when the BusLine has less than two schedules.
    # The minimum length required for a title is 15 spaces.
    # It's needed since terminaltables hides the title if it doesn't fit in the table width.
    # https://github.com/Robpol86/terminaltables/blob/master/terminaltables/build.py  # L73
    if len(bus_line.schedules) <= 2 and len(bus_line.schedules[0].direction) < 15:
        difference = 15 - len(bus_line.schedules[0].direction)
        if difference % 2 != 0:
            difference += 1
        header_blank_spaces = ' ' * (difference // 2)

    for schedule in bus_line.schedules:
        data_table = direction_dict.get(schedule.direction, [])
        if not data_table:
            direction_dict[schedule.direction] = data_table

        header = '{}{}{}'.format(header_blank_spaces, schedule.schedule_day, header_blank_spaces)
        data_table_coloun = [header]
        data_table_coloun.extend(schedule.timetable)
        data_table.append(data_table_coloun)

    for key in direction_dict:
        main_list_table = []
        for line in itertools.zip_longest(*direction_dict[key], fillvalue=''):
            main_list_table.append(list(line))
            actual_table = SingleTable(main_list_table, key)
        output += '{}\n\n'.format(actual_table.table)

    return output


def _build_bus_list_as_table(lines_list, zone):
    output_title = SingleTable([['   List of Bus lines  ({})'.format(zone.title())]])
    output = '{}\n'.format(output_title.table)
    data_table = [['Code', 'Name']]
    for line in lines_list:
        data_table.append([line.code, line.name])

    actual_table = SingleTable(data_table)
    actual_table.inner_row_border = True
    output += '{}\n\n'.format(actual_table.table)
    return str(output)


def _list_to_json(list_of_obj):
    """ Convert a object list to a JSON list """
    output = '{ "list":  %s }' % str(list_of_obj)
    return output


def _run(args):
    """ Run it """

    output_format = args.format if args.format else 'json'

    if args.debug_url:
        pypoabus.DEBUG_URLS = True

    try:
        if args.list:
            lines_list = pypoabus.list_bus_lines(args.list)

            if output_format == 'table':
                table_string = _build_bus_list_as_table(lines_list, args.list)
                _print_stdout(table_string)

            else:
                json_string = _list_to_json(lines_list)
                _print_stdout(json_string)

        elif args.timetable:
            bus_line = pypoabus.get_bus_timetable(args.timetable)

            if output_format == 'table':
                table_string = _build_timetable_as_table(bus_line)
                _print_stdout(table_string)
            else:
                json_string = bus_line.to_json()
                _print_stdout(json_string)

        else:
            _print_stderr('Error when parsing arguments: {}\n'.format(args), True)

    except NoContentAvailableError:
        _print_stderr('Unable to retrieve information from EPTC web site, '
                      'maybe the content is no longer available.\n', True)

    except RemoteServerError as excep:
        _print_stderr('Error to connect to the server: {}\n'.format(excep), True)


def _get_opts():
    """ Function to parse the cmd arguments """

    parser = argparse.ArgumentParser(prog=__title__)
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
