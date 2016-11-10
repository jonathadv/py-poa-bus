""" Entities """

class BusLine():
    """ This is a bus line which has a schedule """

    def __init__(self, name, code):
        """ __init__ """

        self.name = name
        self.code = code
        self.schedule_list = []

    def add_schedule(self, schedule):
        """ method to add a new schedule to the bus """

        self.schedule_list.append(schedule)

    def get_schedule_list(self):
        """ get_schedule_list """

        return self.schedule_list

    def get_name(self):
        """ get_name """

        return self.name

    def get_code(self):
        """ get_code """

        return self.code

    def __str__(self):
        """ to string method """

        string = 'BusLine: %s - %s\n' % (self.code, self.name)
        for sch in self.schedule_list:
            string += 'Direction: %s, Schedule Type: %s\n' % (sch.direction, sch.schedule_day)

            for dep in sch.departures_list:
                string += '%s\n' % dep

        return string

class Schedule():
    """ Class that represents a full bus's schedule"""
    def __init__(self, schedule_day, direction, departures_list):
        """ __init__ """
        self.schedule_day = schedule_day
        self.direction = direction
        self.departures_list = departures_list

    def add_departure_time(self, time):
        """ method to add a new time to depertures list"""
        self.departures_list.append(time)

    def get_schedule_day(self):
        """ get_schedule_day """
        return self.schedule_day

    def get_direction(self):
        """ get_direction """
        return self.direction

    def get_departures_list(self):
        """ get_departures_list """
        return self.departures_list
