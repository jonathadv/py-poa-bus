#!/usr/bin/env python3
import sys
import eptc.eptc_facade as facade
 
line_code = sys.argv[1] if len(sys.argv) > 1 else '101-11'

result = facade.get_bus_line(line_code)


print(result.to_json())


#list_lines= facade.list_bus_lines('south')

#for line in list_lines:
#    print(line)

