#!/usr/bin/env python3
import sys
import eptc_parser.eptc_html_parser as parser

 
line_code = '101-0' if len(sys.argv) < 1 else sys.argv[1]

result = parser.get_bus_line(line_code)


print(result.to_json())

