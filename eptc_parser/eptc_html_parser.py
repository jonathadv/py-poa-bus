"""
This module is the interface between EPTC web site and the application
"""

import re
import requests
from bs4 import BeautifulSoup
from . entities import BusLine, Schedule

def parse_eptc_html(html_doc):
    """
    Function to parse the HTML page.
    It assumes that the HTML follows the below order:
    - Bus line's name and code
    - Direction (origin/destination)
    - Schedule Type (business days, saturday, sunday)

    Example:
       281 - Campo Novo      # Code and Name
       NORTE/SUL             # Origin/Destionation
       Dias Uteis            # Business days
       05:40                 # Time
       05:51                 # Time
       Sabados               # Saturday
       05:40                 # Time
       06:00                 # Time
       Domingos              # Sundays
       06:00                 # Time
       06:24                 # Time
    """
    div_pattern_to_find = 'align="center"><b>'
    time_re = r'(\d\d:\d\d)'
    direction_re = '([A-Z]+/[A-Z]+)'
    day_re = '(Dias Úteis)|(Sábados)|(Domingos)'
    div_list = []

    soup = BeautifulSoup(html_doc, 'html.parser')

    for div in soup.find_all('div'):
        if div_pattern_to_find in str(div):
            div_list.append(div.text)

    if len(div_list) is 0:
        raise Exception('Unable to retrieve information from EPTC web site. '
                        'Please check the bus\' line code and try again.')

    line_title = div_list[0].split('-')
    line_code = line_title[0].strip()
    line_name = line_title[1].strip()

    bus_line = BusLine(line_name, line_code)

    schedule = None
    direction = None

    for i in range(1, len(div_list)):
        if re.match(direction_re, div_list[i].strip()) is not None:
            direction = div_list[i].strip()
            continue

        if re.match(day_re, div_list[i].strip()) is not None:
            schedule = Schedule(div_list[i].strip(), direction, [])
            bus_line.add_schedule(schedule)
            continue

        if re.match(time_re, div_list[i].strip()) is not None:
            schedule.add_departure_time(div_list[i].strip())


    return bus_line



def get_html(url):
    """
    Function to retrieve the HTML Page
    """
    response = requests.get(url)

    if response.status_code is not 200:
        raise Exception('Unable to get EPTC page content. HTTP code: %s, reason: %s' % \
            (response.status_code, response.reason))

    return response.text


def get_bus_line(line_code):
    """
    get_bus_line
    """
    url_eptc = 'http://www.eptc.com.br/EPTC_Itinerarios/Cadastro.asp'
    url_parameters = '?Linha=%s&Tipo=TH&Veiculo=1&Sentido=0&Logradouro=0' % line_code

    html = get_html(url_eptc + url_parameters)

    return parse_eptc_html(html)
