from app.utils import MaintainDates
from tests.BaseTestClass import BaseTestClass
from app.extensions import db
from app.model import User, Morgenmad
import unittest
import datetime


class TestGenerateDates(unittest.TestCase):
    def setUp(self):
        self.dates = MaintainDates(2017, 2018)

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


class TestInsertDatesIntoMorgenmad(BaseTestClass):
    def setUp(self):
        super().setUp()
        self.user = dict(fornavn="Testy", efternavn="Mctesterson", email="test@testing.com", tlf_nr="12345678",
                         password="secret")


        user = User(**self.user)
        db.session.add(user)
        db.session.commit()
        self.dates_util = MaintainDates(2017, 2018)

    def test_user_insertion(self):
        self.dates_util.insert_dates_between_years()
        self.dates_util.users_per_breakfast()
        result = db.session.query(User).first()
        self.assertTrue(result.morgenmad)
        self.assertTrue(len(result.morgenmad) == 104)

    def test_morgenmad_insertion(self):
        self.dates_util.insert_dates_between_years()
        self.dates_util.users_per_breakfast()
        result = db.session.query(Morgenmad).first()
        self.assertTrue(result.user.id == 1)
        self.assertTrue(result.user.email == self.user['email'])

        result = Morgenmad.query.all()
        self.assertTrue(all([friday.user.id == 1 for friday in result]))

