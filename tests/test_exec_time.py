# -*- coding: utf-8 -*-
import os
from unittest import TestCase


from parser.exec_time import ExecTime


class TestExecTimes(TestCase):

    def test_valid_time_split(self):

        expected = {'hour': 16, 'minute': 10}
        response = ExecTime().validate_current_time("16:10")

        self.assertEqual(expected, response, response)


    def test_invalid_input_for_time_split(self):

        expected = {'hour': None, 'minute': None}
        response = ExecTime().validate_current_time("24:60")
        self.assertEqual(expected, response, response)


    def test_invalid_data_type_from_time_split(self):

        expected = {'hour': "12", 'minute': "30"}
        response = ExecTime().validate_current_time("12:30")

        self.assertNotEqual(expected, response, response)

    def test_valid_difference(self):

        response = ExecTime().find_difference(10, 10)
        self.assertEqual(0, response, response)



    def test_find_exec_time_by_split_parameters(self):

        """
        I know it's a bit of a bad practice to 
        do this long of a test-case, but I wanted
        to have some sort of automated test
        to cover this too.
        """
        response = ExecTime().calculate_next_exec(1, 30,
                                                  16, 10,
                                                  ExecTime().find_difference(1, 16),
                                                  ExecTime().find_difference(30, 16))

        self.assertEqual(1, response['hour'], response['hour'])
        self.assertEqual(30, response['minute'], response)
        self.assertEqual('tomorrow', response['day'], response)

