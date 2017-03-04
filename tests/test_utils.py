import datetime
import unittest

from morgenmad.extensions import db
from morgenmad.user.model import User, Morgenmad
from morgenmad.utils import MaintainDates
from morgenmad.config import TestConfig
from tests.BaseTestClass import BaseTestClass


class TestGenerateDates(BaseTestClass):
    def setUp(self):
        super().setUp()

        self.dates = MaintainDates(2017, 2018, config=TestConfig)

    def test_two_years(self):
        dates = [date for date in self.dates.generate_dates()]
        self.assertTrue(len(dates) == 104)
        self.assertTrue(isinstance(dates[0], datetime.date))

    def test_list_weekday(self):
        dates_util = MaintainDates(2017, 2018, weekday=[4])
        dates = [date for date in dates_util.generate_dates()]
        self.assertTrue(len(dates) == 104)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_list_many_weekdays(self):
        dates_util = MaintainDates(2017, 2018, weekday=[0, 4])

        dates = [date for date in dates_util.generate_dates()]
        self.assertTrue(len(dates) == 209)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_weekday_none(self):
        dates_util = MaintainDates(2017, 2018, weekday=None)

        dates = [date for date in dates_util.generate_dates()]
        self.assertTrue(len(dates) == 730)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_tuple_errors(self):
        dates_util = MaintainDates(2017, 2018, weekday=(4,))

        self.assertRaises(TypeError, dates_util.generate_dates())

class TestMaintainDates(BaseTestClass):
    def test_seed_db(self):
        maintain = MaintainDates(config=TestConfig)
        maintain.seed_db()
        self.assertTrue(User.query.get(1) is not None)