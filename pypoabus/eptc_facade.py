# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
This module is the interface between EPTC web site and the application
"""

import json
import re

import pkg_resources
import requests
from bs4 import BeautifulSoup

from .entities import BusLine, BusLineItem, Schedule
from .exceptions import NoContentAvailableError, RemoteServerError


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

    base_url = config.get('eptc_base_url')
    url_action = config.get(action).get('action')

    if action == 'list':
        parameter = config.get(action).get('zones').get(parameter).get('code')

    url_parameters = config.get(action).get('parameters').format(parameter)
    url = '{}/{}?{}'.format(base_url, url_action, url_parameters)

    return url


def parse_timetable_page(html_doc):
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

    if not div_list:
        raise NoContentAvailableError('Unable to retrieve information from EPTC web site. '
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


def adds_missing_tags(html_doc):
    """Fixes a issue in the orginal HTML, where the tag <Option> is not closed..
    Changes from:
    <Select Name=Linha class='ordenacaoSelect'>
        <Option Value='510-87'>510   - AUXILIADORA
        <Option Value='620-5'>520   - TRIANGULO/24 DE OUTUBRO
    To:
    <Select Name=Linha class='ordenacaoSelect'>
        <Option Value='510-87'>510   - AUXILIADORA</Option>
        <Option Value='620-5'>520   - TRIANGULO/24 DE OUTUBRO</Option>
    """
    opened_option_tag = r'<Option'
    closed_option_re = r'</Option>'

    if re.search(closed_option_re, html_doc, re.I) is None:
        html_doc = html_doc.replace(opened_option_tag, closed_option_re + opened_option_tag)

    return html_doc


def parse_bus_list_page(html_doc):
    """
    Function to parse the bus lines names
    """
    bus_line_list = []
    html_doc = adds_missing_tags(html_doc)

    soup = BeautifulSoup(html_doc, 'html.parser')

    for line in soup.find_all('option'):
        line_name = re.sub('[ ]+', ' ', line.text).strip()
        line_code = line.get('value')

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
        raise RemoteServerError('Unable to establish connection.', error)

    if response.status_code != 200:
        raise RemoteServerError('Unable to get EPTC page content. '
                                'HTTP code: {}, reason: {}'
                                .format(response.status_code, response.reason))

    return response.text


def get_bus_timetable(line_code):
    """
    Get timetable from the given bus line
    """
    url = build_url('schedule', line_code)
    html = get_html(url)

    return parse_timetable_page(html)


def list_bus_lines(zone):
    """
    Get all bus lines from a zone
    """
    url = build_url('list', zone)
    html = get_html(url)

    return parse_bus_list_page(html)
