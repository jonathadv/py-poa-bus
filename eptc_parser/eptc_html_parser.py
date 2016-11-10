"""
This module is the interface between EPTC website and the application
"""

import re
import requests
from bs4 import BeautifulSoup
from . entities import BusLine, Schedule

def parse_eptc_html(html_doc):
    """
    Function to parse the HTML page
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
    if 'http://www.eptc.com.br/EPTC_Itinerarios' not in url:
        raise ValueError('The URL send does not seem to be from EPTC')

    response = requests.get(url)

    if response.status_code is not 200:
        raise Exception('Unable to get EPTC page content. HTTP code: %s, reason: %s' % \
            (response.status_code, response.reason))

    return response.text


def main(url):
    """
    Main Function
    """
    html = get_html(url)

    return parse_eptc_html(html)
