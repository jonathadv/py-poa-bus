# PyPoABus

Application to retrieve the bus schedules of Porto Alegre city.

* **List bus lines by zone: north, south, east, public (from Carris company)**
* **Retrieve timetables by bus line**


Data source: www.eptc.com.br


## Why that?

As far as I know, the Porto Alegre city hall doesn't provide an API to get the oficial information about bus schedules. The idea here is to provide at least a interface that allows us to convert the online information from EPTC web site to JSON representation.


## Usage

**List bus lines**

```Python
>>> import eptc.eptc_facade as facade
>>> zone = 'south'
>>> list_bus_lines = facade.list_bus_lines(zone)
>>> for i in list_bus_lines:
...     print(i)
... 
{"code": "210-14", "name": "110 - RESTINGA NOVA VIA TRISTEZA"}
{"code": "210-81", "name": "1101 - RESTINGA NOVA VIA TRISTEZA/DOMINGOS E FERIADOS"}
{"code": "210-46", "name": "1102 - RESTINGA NOVA VIA TRISTEZA/BARRA SHOPPING"}
{"code": "211-11", "name": "111 - RESTINGA VELHA (TRISTEZA)"}
{"code": "211-12", "name": "1111 - RESTINGA VELHA(TRISTEZA)/SHOPPING"}
{"code": "272-33", "name": "1112 - HIPICA/TRISTEZA"}

```

**Get bus line timetable**

```Python
>>> import eptc.eptc_facade as facade
>>> bus_line_code = '281-1'
>>> timetable = facade.get_bus_timetable(bus_line_code)
>>> timetable.code
'2811'
>>> timetable.name
'CAMPO NOVO / MORRO AGUDO'
>>> timetable.to_json()
'{"code": "2811", "name": "CAMPO NOVO / MORRO AGUDO", "schedules": [{"direction": "BAIRRO/CENTRO", "schedule_day": "Dias Úteis", "timetable": ["05:30", "06:00", "06:30", "06:55", "07:25", "07:45", "09:00", "09:55", "10:35", "11:00", "11:35", "12:35", "13:30", "14:10", "14:40", "15:45", "16:25", "17:55", "19:10", "20:30", "21:30", "22:25"]}, {"direction": "BAIRRO/CENTRO", "schedule_day": "Sábados", "timetable": ["06:15", "06:55", "07:45", "08:30", "10:20", "11:20", "13:35", "14:25", "15:40", "16:55", "18:10", "19:25", "21:05", "22:45"]}, {"direction": "CENTRO/BAIRRO", "schedule_day": "Dias Úteis", "timetable": ["06:20", "06:50", "08:05", "08:25", "08:45", "10:00", "10:55", "11:35", "12:00", "12:35", "13:35", "14:30", "15:10", "15:40", "16:45", "17:25", "17:50", "18:45", "18:55", "20:00", "22:15", "23:10"]}, {"direction": "CENTRO/BAIRRO", "schedule_day": "Sábados", "timetable": ["07:05", "07:45", "08:35", "09:20", "10:05", "11:10", "12:10", "14:25", "15:15", "16:30", "20:15", "21:50", "23:30"]}]}'
>>> 


```


## CMD Tool

This tool allows the user to access some features of PyPoaBus without to code a new module or Python script. It handles `stdout` and `stderr` messages, so `|` (pipe) can be used to send the output to another handler.

The below examples are using `jq` (https://stedolan.github.io/jq/) to format the JSON output.


#### Help

```bash
bash~$ ./cmd.py

usage: cmd.py [-h] [--list zone | --timetable line_code] [-v format]

optional arguments:
  -h, --help            show this help message and exit
  --list zone           [north|south|east|public]
  --timetable line_code
                        Line code like 281-1, 101-1, etc.Use --list to get
                        line codes.
  -v format, --view format
                        [json|table]

```
#### Examples



**List bus lines**

```bash
bash~$ ./cmd.py --list south -v json | jq  # jq is only a external tool to format json (not included) :D
```
```JavaScript
{
  "list": [
    {
      "code": "210-14",
      "name": "110 - RESTINGA NOVA VIA TRISTEZA"
    },
    {
      "code": "210-81",
      "name": "1101 - RESTINGA NOVA VIA TRISTEZA/DOMINGOS E FERIADOS"
    },
    {
      "code": "210-46",
      "name": "1102 - RESTINGA NOVA VIA TRISTEZA/BARRA SHOPPING"
    },
    {
      "code": "211-11",
      "name": "111 - RESTINGA VELHA (TRISTEZA)"
    }
}
```

```bash
bash~$ ./cmd.py --list south -v table # format output as table
```
```bash
Line Code    Line Name
----------------------------------------
210-14       110 - RESTINGA NOVA VIA TRISTEZA
210-81       1101 - RESTINGA NOVA VIA TRISTEZA/DOMINGOS E FERIADOS
210-46       1102 - RESTINGA NOVA VIA TRISTEZA/BARRA SHOPPING
211-11       111 - RESTINGA VELHA (TRISTEZA)
211-12       1111 - RESTINGA VELHA(TRISTEZA)/SHOPPING
272-33       1112 - HIPICA/TRISTEZA
149-0        149 - ICARAI
149-1        1491 - ICARAI(ALTO TAQUARI)
265-0        165 - COHAB
268-11       168 - BELEM NOVO(VIA TRISTEZA)
```


**Get bus line timetable**

```bash
bash~$ ./cmd.py --timetable 281-81 | jq # jq is only a external tool to format json (not included) :D
```
```JavaScript
{
  "code": "R81",
  "name": "RAPIDA CAMPO NOVO",
  "schedules": [
    {
      "direction": "BAIRRO/CENTRO",
      "schedule_day": "Dias Úteis",
      "timetable": [
        "06:25",
        "06:45",
        "07:05",
        "07:25",
        "07:40",
        "08:00"
      ]
    },
    {
      "direction": "CENTRO/BAIRRO",
      "schedule_day": "Dias Úteis",
      "timetable": [
        "17:20",
        "17:45",
        "18:15"
      ]
    }
  ]
}
```



