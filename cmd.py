#!/usr/bin/env python3

import sys, argparse
import eptc.eptc_facade as facade

def run(args):    
    if args.list is not None:
        lines_list= facade.list_bus_lines(args.list)
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
        ArgumentError('Error when parsing arguments')
    


def main():

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()    
    group.add_argument('--list', required=False,
                                 metavar='zone', \
                                 help='[north|south|east|public]', \
                                 choices=['north', 'south', 'east', 'public'])
    group.add_argument('--timetable', required=False,
                                      metavar='line_code', 
                                      help='Line code like 281-1, '
                                      '101-1, etc.' 'Use --list to get line codes.')

    args = parser.parse_args()

    if(len(sys.argv) <= 1):
        parser.print_help()
        
    else:
        run(args)
        

        
main()
