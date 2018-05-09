#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

""" CMD Helper Script """

import argparse
import sys
from collections import OrderedDict

from . import eptc_facade as facade
from .exceptions import NoContentAvailableException, RemoteServerErrorException


def print_err(message, exit_cmd=False):
    """ Functionto close the cmd """
    print('cmd: %s' % message, file=sys.stderr)

    if exit_cmd:
        sys.exit(1)


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


def generate_table(title, data):
    """
        Function to generate a table from
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

    table_string = '\n\t' * int(columns_number/2) + title + '\n\n'
    table_string += line_template % tuple([key for key in data.keys()])
    table_string += '------------------------' * columns_number + '\n'

    for i in range(0, max_column_length):
        table_string += line_template % get_table_line(data, i)

    print(table_string)


def list_to_json(list_of_obj):
    """ Convert a object list to a JSON list """
    output = '{ "list":  %s  }' % str(list_of_obj)
    print(output)


def run(args):
    """ Run it """

    view = args.view if args.view is not None else 'json'

    try:
        if args.list is not None:
            lines_list = facade.list_bus_lines(args.list)

            if view == 'table':
                line_names = [line.name for line in lines_list]
                line_codes = [line.code for line in lines_list]

                data = OrderedDict()
                data['Code'] = line_codes
                data['Name'] = line_names

                title = 'List of Bus lines'
                generate_table(title, data)

            else:
                list_to_json(lines_list)

        elif args.timetable is not None:
            timetable = facade.get_bus_timetable(args.timetable)

            if view == 'table':
                for sched in timetable.schedules:
                    data = OrderedDict()
                    data['Time'] = sched.timetable

                    title = '%s - %s | %s | %s' % (timetable.code,
                                                   timetable.name,
                                                   sched.schedule_day,
                                                   sched.direction)
                    generate_table(title, data)

            else:
                print(timetable.to_json())

        else:
            print_err('Error when parsing arguments: %s' % args, True)


    except NoContentAvailableException:
        print_err('Unable to retrieve information from EPTC web site, '
                  'maybe the content is no longer available. Args = [%s]\n' % args, True)

    except RemoteServerErrorException as excep:
        print_err('Error to connect to the server: %s ' % excep, True)



def main():
    """ Main function """

    parser = argparse.ArgumentParser(prog='pypoabus')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', required=False,
                       metavar='zone',
                       help='[north|south|east|public]',
                       choices=['north', 'south', 'east', 'public'])

    group.add_argument('--timetable', required=False,
                       metavar='line_code',
                       help='Line code like 281-1, '
                       '101-1, etc.' 'Use --list to get line codes.')

    parser.add_argument('-v', '--view', metavar='format',
                        help='[json|table]',
                        required=False,
                        choices=['json', 'table'])

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()

    else:
        run(args)



main()
