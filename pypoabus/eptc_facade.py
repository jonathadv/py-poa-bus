# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
This module is the interface between EPTC web site and the application
"""

import json
import re
import requests
import pkg_resources
from bs4 import BeautifulSoup
from . entities import BusLineItem, BusLine, Schedule
from . exceptions import NoContentAvailableException, RemoteServerErrorException

def load_config():
    """ Function to open configuration file """
    config_file = 'config.json'
    conf_file = open(pkg_resources.resource_filename(__package__, config_file))
    config = json.load(conf_file)

    return config


def build_url(action, parameter):
    """ Function to build URL using information
    from config.json file """
    config = load_config()

    base_url = config['eptc_base_url']
    url_action = config[action]['action']

    if action is 'list':
        parameter = config[action]['zones'][parameter]['code']

    url_parameters = config[action]['parameters'] % parameter

    url = '%s/%s?%s' % (base_url, url_action, url_parameters)

    return url


def parse_schedule_page(html_doc):
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
        raise NoContentAvailableException('Unable to retrieve information from EPTC web site. '
                                          'Please check the bus line code and try again.')

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


def parse_bus_list_page(html_doc):
    """ Function to parse the bus lines names  """
    opened_option_tag = '<Option'
    closed_option_re = r'</option>'
    bus_line_list = []

    if re.search(closed_option_re, html_doc, re.I) is None:
        html_doc = html_doc.replace(opened_option_tag, closed_option_re + opened_option_tag)

    soup = BeautifulSoup(html_doc, 'html.parser')

    for line in soup.find_all('option'):
        line_name = re.sub('[ ]+', ' ', line.text).strip()
        line_code = line['value']

        bus_line = BusLineItem(line_code, line_name)
        bus_line_list.append(bus_line)

    return bus_line_list


def get_html(url):
    """
    Function to retrieve the HTML Page
    """
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as error:
        raise RemoteServerErrorException('Unable to establish connection.', error)

    if response.status_code is not 200:
        raise RemoteServerErrorException('Unable to get EPTC page content. '
                                         'HTTP code: %s, reason: %s' % \
            (response.status_code, response.reason))

    return response.text


def get_bus_timetable(line_code):
    """
    Get timetable from the given bus line
    """

    url = build_url('schedule', line_code)
    html = get_html(url)

    return parse_schedule_page(html)


def list_bus_lines(zone):
    """
    Get all bus lines from a zone
    """
    url = build_url('list', zone)
    html = get_html(url)

    return parse_bus_list_page(html)
