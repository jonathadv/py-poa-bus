# PyPoABus

Application to retrieve the bus lines' timetables of Porto Alegre city.

* **List bus lines by zone: north, south, east, public (from Carris company)**
* **Retrieve timetables by bus line**


Data source: www.eptc.com.br


## Why that?

As far as I know, the Porto Alegre city hall doesn't provide an API to get the oficial information about bus lines' timetables. The idea here is to provide at least a interface that allows us to convert the online information from EPTC web site to a JSON representation.


### CMD Tool

This tool allows the user to access some features of PyPoaBus without the need of importing the module to another application or Python console.

```bash
bash~$ ./cmd.py

usage: cmd.py [-h] [--list zone | --timetable line_code]

optional arguments:
  -h, --help            show this help message and exit
  --list zone           [north|south|east|public]
  --timetable line_code
                        Line code like 281-1, 101-1, etc.Use --list to get
                        line codes.

```

