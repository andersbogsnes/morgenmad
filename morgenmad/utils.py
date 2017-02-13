from itsdangerous import URLSafeTimedSerializer
from morgenmad.config import BaseConfig
from flask_mail import Message
from morgenmad.extensions import mail
from morgenmad.user.model import Morgenmad, User
from datetime import date, timedelta
from itertools import cycle
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import pathlib


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECRET_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECRET_SALT,
            max_age=expiration)
    except:
        return False
    return email


def send_confirmation_email(to, subject, template):
    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=BaseConfig.MAIL_DEFAULT_SENDER)
    mail.send(msg)


def next_friday():
    d = date.today()
    while d.weekday() != 4:
        d = d + timedelta(days=1)
    return d


class MaintainDates:
    """Container class for all utilities for maintain Dates in the database.
    :param start_year: Year to begin counting. Inclusive
    :param end_year: Year to end counting. Inclusive
    :param weekday: Default 4 = Friday. Weekdays indexed from 0. Also accepts lists of weekdays
     """

    def __init__(self, start_year=None, end_year=None, weekday=4, config=BaseConfig):
        self.start_year = start_year or date.today().year
        self.end_year = end_year or self.start_year + 1
        self.weekday = weekday
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.session = sessionmaker(bind=self.engine)()

    def generate_dates(self):
        """Helper to generate every given weekday between start_year and end_year
        """

        start_date = date(self.start_year, 1, 1)
        end_date = date(self.end_year, 12, 31)
        delta = end_date - start_date

        for day in range(delta.days + 1):
            new_date = start_date + timedelta(day)
            if isinstance(self.weekday, int):
                if new_date.weekday() == self.weekday:
                    delta_day = new_date
                else:
                    continue

            elif isinstance(self.weekday, list):
                if new_date.weekday() in self.weekday:
                    delta_day = new_date
                else:
                    continue
            elif self.weekday is None:
                delta_day = new_date
            else:
                raise TypeError("Weekday must be one of list, int or None")

            yield delta_day

    def insert_dates_between_years(self):
        """Inserts all dates generated in the interval"""
        for given_date in self.generate_dates():
            if not self.session.query(Morgenmad).filter_by(dato=given_date).first():
                morgenmad = Morgenmad(dato=given_date)
                self.session.add(morgenmad)
            self.session.commit()

    def users_per_breakfast(self):
        unassigned_breakfast = self.session.query(Morgenmad).filter(Morgenmad.user == None).all()
        all_users = self.session.query(User).order_by(User.id).all()
        for breakfast, user in zip(unassigned_breakfast, cycle(all_users)):
            breakfast.user = user
            self.session.add(breakfast)
        self.session.commit()

    def set_active_morgenmad(self):
        last_breakfast = self.session.query(Morgenmad).filter(Morgenmad.is_next).first()
        if last_breakfast:
            last_breakfast.is_next = False
            self.session.add(last_breakfast)
        next_breakfast = self.session.query(Morgenmad).filter(Morgenmad.dato == next_friday()).first()
        next_breakfast.is_next = True
        self.session.add(next_breakfast)
        self.session.commit()

    def seed_db(self):
        users_json = pathlib.Path(BaseConfig.PROJECT_DIR).joinpath('seed_users.json')
        self.seed_users(users_json)
        self.insert_dates_between_years()
        self.users_per_breakfast()
        self.set_active_morgenmad()

    def update_db(self):
        self.insert_dates_between_years()
        self.users_per_breakfast()
        self.set_active_morgenmad()

    @staticmethod
    def seed_users(users_json, config=BaseConfig):
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        path = pathlib.Path(users_json)
        if not path.exists():
            raise FileNotFoundError(f"Invalid path to users_json: {str(path)}")
        with path.open(encoding='latin-1') as p:
            users = json.load(p)
        for user in users:
            new_user = User(**user)
            session.add(new_user)
        session.commit()
