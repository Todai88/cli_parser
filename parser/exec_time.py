import logging
import sys

from cli_parser import CliParser

class ExecTime(object):

    def __init__(self):
        self.logger = logging.Logger(u'execution times')
        self.logger.setLevel(logging.WARNING) # we want to display warnings by default
        self.values = {'min': 0, 'max_hour': 23, 'max_min': 59}

    def find_exec_times(self, curr_time, path = None, str = None, verbose = False):
        """
        If given correct parameter values 
        it will find the next execution time(s)
        :param curr_time: 
        :param path: 
        :param str: 
        :return: 
        """

        exec_times = []

        validated_current_time = self.validate_current_time(curr_time)

        if validated_current_time.get('minute') and validated_current_time.get('hour'):

            # first checking if file path supplied:

            if path and not str:
                data = (
                    CliParser(self.logger, verbose).check_and_parse_file(path)
                )
            else: ## parse from string
                data = (
                    CliParser(self.logger, verbose).check_and_parse_string(str)
                )

            for entry in data:
                ## using timedelta to find differences in hour, min

                hour_difference = self.find_difference(
                    entry.get('hour'), validated_current_time.get('hour')
                )

                minute_difference = self.find_difference(
                    entry.get('minute'), validated_current_time.get('minute')
                )

                next_exec = self.calculate_next_exec(
                    entry.get('hour'), entry.get('minute'),
                    validated_current_time.get('hour'), validated_current_time.get('minute'),
                    hour_difference, minute_difference
                )

                exec_times.append([
                    self.format_time(next_exec.get('hour'), next_exec.get('minute')),
                    next_exec.get('day'), entry.get('path')
                ])

            return exec_times

    def validate_current_time(self, time):
        """
        Given correctly formatted time
        returns separated time
        :param time: 
        :return: dictionary representation 
                 of time
        """

        validated_hour = None
        validated_minute = None

        # getting the time

        hour, minute = time.split(":")
        try:
            if ((self.values['min'] <= int(hour) <= self.values['max_hour']) and
                    (self.values['min'] <= int(minute) <= self.values['max_min'])):

                validated_hour = int(hour)
                validated_minute = int(minute)

        except ValueError as exception:
            logging.error("""
            Supplied time is invalid...
            Error: %s""", exception)

        validated_time = {'hour': validated_hour, 'minute': validated_minute}

        return validated_time


    def find_difference(self, entry, current):
        """
        Find the difference between
        entry and current
        :param entry: 
        :param current: 
        :return: a numeric representation of
                 the difference
        """

        if not str(entry).strip() == '*':
            return (int(entry) - int(current))

        return 0

    def format_time(self, hour, min):
        """
        Formats the time
        :param hour: 
        :param min: 
        :return: A formatted time string
        """


        minute = (min if min > 9 else '0' + str(min))

        return ':'.join([str(hour), str(minute)])

    def calculate_next_exec(self, entry_hour, entry_min,
                    curr_hour, curr_min,
                    hour_difference, minute_difference):

        """
        Attempts to calculate the next 
        execution time based on the 
        supplied arguments
        :param entry_hour: 
        :param entry_min: 
        :param curr_hour: 
        :param curr_min: 
        :param hour_difference: 
        :param minute_difference: 
        :return: the next time and day
        """


        if entry_hour == '*' and entry_min == '*':
            ## It will run next possible time, now.

            next_exec_hour = curr_hour
            next_exec_min = curr_min
            next_exec_day = 'today'

        elif entry_hour == '*':
            ## checking if hour is every hour

            if minute_difference < 0:
                ## we know there is a difference

                if curr_hour == self.values.get('max_hour'):
                    ## is last hour of day

                    next_exec_day = 'tomorrow'
                    next_exec_hour = 0

                else:
                    next_exec_hour = curr_hour + 1
                    next_exec_day = 'today'

            else:
                next_exec_hour = curr_hour
                next_exec_day = 'today'

            next_exec_min = entry_min

        elif entry_min == '*':
            ## minute is every minute

            if hour_difference < 0:
                next_exec_min = 0
                next_exec_day = 'tomorrow'

            elif hour_difference == 0:
                next_exec_min = curr_min
                next_exec_day = 'today'

            else:
                next_exec_min = 0
                next_exec_day = 'today'

            next_exec_hour = entry_hour

        else:

            ## we know both entries are specified

            if hour_difference < 0:
                next_exec_day = 'tomorrow'
            elif hour_difference == 0:
                if minute_difference < 0:
                    next_exec_day = 'tomorrow'
                else:
                    next_exec_day = 'today'
            else:
                next_exec_day = 'today'

            next_exec_hour = entry_hour
            next_exec_min = entry_min

        return {
            'day': next_exec_day,
            'hour': next_exec_hour,
            'minute': next_exec_min
        }
