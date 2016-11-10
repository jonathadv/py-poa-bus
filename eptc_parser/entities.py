""" Entities """
import json

class BusLine():
    """ This is a bus line which has a schedule """

    def __init__(self, name, code):
        """ __init__ """

        self.name = name
        self.code = code
        self.schedules = []

    def add_schedule(self, schedule):
        """ method to add a new schedule to the bus """

        self.schedules.append(schedule)

    def get_schedule_list(self):
        """ get_schedules """

        return self.schedules

    def get_name(self):
        """ get_name """

        return self.name

    def get_code(self):
        """ get_code """

        return self.code

    def to_json(self):
        """ Generates JSON representation"""
        return json.dumps(self.__dict__, sort_keys=True, cls=ComplexEncoder)

    def __str__(self):
        """ to string method """

        string = 'BusLine: %s - %s\n' % (self.code, self.name)
        for sch in self.schedules:
            string += 'Direction: %s, Schedule Type: %s\n' % (sch.direction, sch.schedule_day)

            for dep in sch.departures:
                string += '%s\n' % dep

        return string


class Schedule():
    """ Class that represents a full bus's schedule"""
    def __init__(self, schedule_day, direction, departures):
        """ __init__ """
        self.schedule_day = schedule_day
        self.direction = direction
        self.departures = [] if departures is None else departures

    def add_departure_time(self, time):
        """ method to add a new time to depertures list"""
        self.departures.append(time)

    def get_schedule_day(self):
        """ get_schedule_day """
        return self.schedule_day

    def get_direction(self):
        """ get_direction """
        return self.direction

    def get_departures(self):
        """ get_departures """
        return self.departures

    def to_json(self):
        """ Generates JSON representation"""
        return json.dumps(self.__dict__, sort_keys=True, cls=ComplexEncoder)


class ComplexEncoder(json.JSONEncoder):
    """ Helper class to enable JSON convertion """
    def default(self, obj):
        """ This is the default method"""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
