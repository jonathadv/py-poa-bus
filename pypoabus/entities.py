# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# pylint: disable=method-hidden
# pylint: disable=too-few-public-methods



""" Entities """


import json


class JSONSerializable():
    """ Class to simplify the JSON serialization """

    def __json_dict__(self):
        """ Method to remove _ (underscore) from beggining of the attribute name """
        simple_dict = self.__dict__.copy()

        for key in simple_dict.keys():
            if key.startswith('_'):
                new_key = key[1:]
                simple_dict[new_key] = simple_dict[key]
                del simple_dict[key]

        return simple_dict


    def to_json(self):
        """ Generates JSON representation"""
        return json.dumps(self.__json_dict__(), sort_keys=True,
                          cls=ComplexEncoder, ensure_ascii=False)




class BusLineItem(JSONSerializable):
    """ This class represents a bus line """

    def __init__(self, code, name):
        """ __init__  """
        self._code = code
        self._name = name

    @property
    def code(self):
        """ getter method """
        return self._code

    @code.setter
    def code(self, value):
        """ setter method """
        self._code = value

    @property
    def name(self):
        """ getter method """
        return self._name

    @name.setter
    def name(self, value):
        """ setter method """
        self._name = value

    def __repr__(self):
        """ Representation to this class """
        return self.__str__()

    def __str__(self):
        """ to string method """
        return self.to_json()


class BusLine(JSONSerializable):
    """ This is a bus line which has a schedule """

    def __init__(self, name, code):
        """ __init__ """
        self._name = name
        self._code = code
        self._schedules = []

    def add_schedule(self, schedule):
        """ method to add a new schedule to the bus """
        self._schedules.append(schedule)

    @property
    def schedules(self):
        """ schedules getter """
        return self._schedules

    @property
    def name(self):
        """ name getter """
        return self._name

    @property
    def code(self):
        """ code getter """
        return self._code

    def __str__(self):
        """ to string method """

        string = 'BusLine: %s - %s\n' % (self._code, self._name)
        for sch in self._schedules:
            string += 'Direction: %s, Schedule Type: %s\n' % (sch.direction, sch.schedule_day)

            for deperture in sch.timetable:
                string += '%s\n' % deperture

        return string


class Schedule(JSONSerializable):
    """ Class that represents a full bus's schedule"""
    def __init__(self, schedule_day, direction, departures):
        """ __init__ """
        self._schedule_day = schedule_day
        self._direction = direction
        self._timetable = [] if departures is None else departures

    def add_departure_time(self, time):
        """ method to add a new time to depertures list"""
        self._timetable.append(time)

    @property
    def schedule_day(self):
        """ schedule_day getter """
        return self._schedule_day

    @property
    def direction(self):
        """ direction getter """
        return self._direction

    @property
    def timetable(self):
        """ timetable getter"""
        return self._timetable

    def  __str__(self):
        """ to string method """
        return self.to_json()



class ComplexEncoder(json.JSONEncoder):
    """ Helper class to enable JSON convertion """
    def default(self, o):
        """ This is the default method"""
        if hasattr(o, '__json_dict__'):
            return o.__json_dict__()

        return json.JSONEncoder.default(self, o)
