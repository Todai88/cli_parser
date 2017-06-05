# -*- coding: utf-8 -*-
import os
from unittest import TestCase


from parser.cli_parser import CliParser


class TestCronParser(TestCase):

    def setUp(self):
        self.THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_valid_data_from_string(self):
        """
        Just testing the one line as there is a risk that
        the dictionary gets bundled and test fails.
        """
        response = CliParser(None).check_and_parse_string("30 1 /bin/run_me_daily")
        expected = [{'path': '/bin/run_me_daily', 'hour': 1, 'minute': 30}]

        self.assertEqual(expected, response, "String missmatch: \n" + str(response))

    
