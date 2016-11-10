#!/usr/bin/env python3

t11_page = '101-1'

import eptc_parser.eptc_html_parser as parser
result = parser.get_bus_line(t11_page)

print(result)

