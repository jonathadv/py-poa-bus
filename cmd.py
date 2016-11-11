#!/usr/bin/env python3
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

""" CMD Helper Script """

import argparse
import sys
import eptc.eptc_facade as facade
from eptc.eptc_facade import NoContentAvailableException

def run(args):
    """ Run it """
    try:
        if args.list is not None:
            lines_list = facade.list_bus_lines(args.list)
            output = '{0:<12} {1}\n'.format('Line Code', 'Line Name')
            output += '-' * 40
            output += '\n'
            for line in lines_list:
                output += ('{0:<12} {1}\n'.format(line.code, line.name))

            print(output)

        elif args.timetable is not None:
            timetable = facade.get_bus_line(args.timetable)
            print(timetable.to_json())

        else:
            raise ValueError('Error when parsing arguments')

    except NoContentAvailableException:
        print('cmd: Unable to retrieve information from EPTC web site, '
              'maybe the content is no longer available.\n')



def main():
    """ Main function """

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', required=False,
                       metavar='zone',
                       help='[north|south|east|public]',
                       choices=['north', 'south', 'east', 'public'])
    group.add_argument('--timetable', required=False,
                       metavar='line_code',
                       help='Line code like 281-1, '
                       '101-1, etc.' 'Use --list to get line codes.')

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()

    else:
        run(args)



main()
