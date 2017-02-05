from app.utils import generate_dates, insert_dates_into_morgenmad
from tests.BaseTestClass import BaseTestClass
from app.extensions import db
from app.model import User, Morgenmad
import unittest
import datetime


class TestGenerateDates(unittest.TestCase):
    def test_two_years(self):
        start_year = 2017
        end_year = 2018

        dates = [date for date in generate_dates(start_year, end_year)]
        self.assertTrue(len(dates) == 104)
        self.assertTrue(isinstance(dates[0], datetime.date))

    def test_list_weekday(self):
        start_year = 2017
        end_year = 2018

        dates = [date for date in generate_dates(start_year, end_year, weekday=[4])]
        self.assertTrue(len(dates) == 104)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_list_many_weekdays(self):
        start_year = 2017
        end_year = 2018

        dates = [date for date in generate_dates(start_year, end_year, weekday=[0, 4])]
        self.assertTrue(len(dates) == 209)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_weekday_none(self):
        start_year = 2017
        end_year = 2018

        dates = [date for date in generate_dates(start_year, end_year, weekday=None)]
        self.assertTrue(len(dates) == 730)
        self.assertTrue(isinstance(dates[0], datetime.date))
        self.assertTrue(dates[0].year == 2017)
        self.assertTrue(dates[0].month == 1)

    def test_tuple_errors(self):
        start_year = 2017
        end_year = 2018

        self.assertRaises(TypeError, generate_dates(start_year, end_year, weekday=(4,)))


class TestInsertDatesIntoMorgenmad(BaseTestClass):
    def setUp(self):
        super().setUp()
        user = User(**self.user)
        db.session.add(user)
        db.session.commit()

    def test_user_insertion(self):
        insert_dates_into_morgenmad(2017, 2018)
        result = User.query.first()
        self.assertTrue(result.morgenmad)
        self.assertTrue(len(result.morgenmad) == 104)

    def test_morgenmad_insertion(self):
        insert_dates_into_morgenmad(2017, 2018)
        result = Morgenmad.query.first()
        self.assertTrue(result.user.id == 1)
        self.assertTrue(result.user.email == self.user['email'])

        result = Morgenmad.query.all()
        self.assertTrue(all([friday.user.id == 1 for friday in result]))

