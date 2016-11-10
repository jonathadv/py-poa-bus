import requests
import re
from bs4 import BeautifulSoup




'''
Classes
'''
class BusLine():
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.schedule_list = [] 
    
    def add_schedule(self, schedule):
        self.schedule_list.append(schedule)

    def __str__(self):
        string = 'BusLine: %s - %s\n' % (self.code, self.name)
        for sch in self.schedule_list:
            string += 'Direction: %s, Schedule Type: %s\n' % (sch.direction, sch.schedule_day)
            
            for dep in sch.departures_list:
                string += '%s\n' % dep

        return string

class Schedule():
    def __init__(self, schedule_day, direction, departures_list):
        self.schedule_day = schedule_day
        self.direction = direction
        self.departures_list = departures_list

    def add_departure_time(self, time):
        self.departures_list.append(time)



'''
Function to parse the HTML page
'''
def parse_eptc_html(html_doc):
    div_pattern_to_find = 'align="center"><b>'
    time_re = '(\d\d:\d\d)'
    direction_re = '([A-Z]+/[A-Z]+)'
    day_re='(Dias Úteis)|(Sábados)|(Domingos)'
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



'''
Function to retrieve the HTML Page
'''            
def get_html(url):
    
    if 'http://www.eptc.com.br/EPTC_Itinerarios' not in url:
        raise ValueError('The URL send does not seem to be from EPTC')
    
    response = requests.get(url)
    
    if response.status_code is not 200:
        raise Exception('Unable to get EPTC page content. HTTP code: %s, reason: %s' % (response.status_code, response.reason))
    
    return response.text


'''
Main Function
'''
def main(url):
    html = get_html(url)

    return parse_eptc_html(html)

