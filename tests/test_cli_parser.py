# -*- coding: utf-8 -*-
import os
from unittest import TestCase


from parser.cli_parser import CliParser


class TestCronParser(TestCase):

    def setUp(self):
        self.THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_valid_path(self):
        file_path = os.path.join(self.THIS_DIR, 'basic_tests.txt')
        expected = True
        response = CliParser(None).is_valid_path(file_path)

        self.assertEqual(expected, response, "Incorrect PATH")

    def test_invalid_path(self):
        file_path = os.path.join(self.THIS_DIR, 'this_directory_will_fail.txt')
        expected = False
        response = CliParser(None).is_valid_path(file_path)

        self.assertEqual(expected, response, "Incorrect PATH")

    def test_get_cron_data(self):
        file_path = os.path.abspath(u'crontab.txt')
        expected = [
            u'30 1 /bin/run_me_daily',
            u'45 * /bin/run_me_hourly',
            u'* * /bin/run_me_every_minute',
            u'* 19 /bin/run_me_sixty_times'
        ]
        response = CliParser(None).get_data_from_file(file_path)