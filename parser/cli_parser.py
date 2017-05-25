# -*- coding: utf-8 -*-

import os #as we need path


class CliParser(object):

    def __init__(self, verbose, logger = None):
        ## Adding a logger to follow along and print warnings / errors.
        ## Verbose to write debug info

        self.logger = logger
        self.verbose = verbose

    def check_and_parse_file(self, path):
        """
        Returns a dictionary of parsed data
        if file exists and can be correctly formatted
        :param path: 
        :return: list of dictionaries
        """

        pretty_data = []

        if self.is_valid_path(path):
            if self.verbose:
                print(">>> File exists.")

            to_parse = self.get_data_from_file(path)
            if self.verbose:
                print(">>> Got the text")

            parsed_data = self.parse_data(to_parse)
            if self.verbose:
                print(">>> Parsed the text")

            pretty_data = self.format_data(parsed_data)
            if self.verbose:
                print(">>> Formatted the data")

        return pretty_data


    def check_and_parse_string(self, data_string):
        """
        Returns a dictionary of parsed data
        if string can be correctly formatted
        :param string: 
        :return: list of formatted exec dictionaries
        """

        if self.verbose:
            print(">>> You supplied a string")

        if data_string:

            parsed_data = self.parse_data(data_string.split('\\n'))
            if self.verbose:
                print(">>> Parsed the text")

            pretty_data = self.format_data(parsed_data)
            if self.verbose:
                print(">>> Formatted the data")

    def is_valid_path(self, path):
        """
        Check if a file exists in path
        :return: boolean indicating success or failure
        """
        return os.path.isfile(path)

    def get_data_from_file(self, path):
        """
        Gets data from a file by 
        reading line for line.
        :param path: 
        :return: a list of newline separated 
                 strings
        """

        data_list = []

        try:
            with open(path, 'r') as f:
                for line in f:
                    data_list.append(line.strip('\n')) # remove newline symbol
        except IOError as exception:
            if self.logger:
                self.logger.error("""
                Could not successfully read file..
                Exception: %s""", exception)

        return data_list

    def parse_data(self, data):
        """
        Split data into list of exec entries
        :param data: 
        :return: List of split entries list
        """

        liat_of_entries_list = []

        for entry in data:
            try:
                entry_list = entry.strip().split()
                liat_of_entries_list.append(entry_list)
            except ValueError as exception:
                if self.logger:
                    self.logger.error("""
                    Could not successfully process list..
                    Exception: %s""", exception)

        return liat_of_entries_list

    def format_data(self, data):
        """
        Attempts to createa a dictionary based
        on data.
        :param data: 
        :return: A dictionary list of formatted
                 exec entries
        """

        formatted_exec_dictionary_list = []

        for entry in data:
            try:
                formatted_exec = {
                    'minute': self.validate_type_and_range(entry[0]),
                    'hour': self.validate_type_and_range(entry[1]),
                    'fun': entry[2]
                }
                formatted_exec_dictionary_list.append(formatted_exec)
            except IndexError as exception:
                if self.logger:
                    self.logger.error("""
                    Could not successfully parse entry...
                    Exception: %s""", exception)

            return formatted_exec_dictionary_list

    def validate_type_and_range(self, to_check, low, high):
        """
        Check if a value is numeric and in range
        :param to_check: 
        :param low: 
        :param high: 
        :return: Correct numerical value, * or None
        """

        try:

            if to_check == '*':
                return to_check
            if low <= int(to_check) <= high:
                return int(to_check)

        except ValueError as exception:
            if self.logger:
                self.logger.error(""" 
                Value is either not numerical, or out of bounds...
                Exception: %s""", exception)

        return None



