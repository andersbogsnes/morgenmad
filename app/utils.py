from itsdangerous import URLSafeTimedSerializer
from app.config import BaseConfig
from flask_mail import Message
from app.extensions import mail
from app.model import Morgenmad, User
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


class MaintainDates:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
        self.session = sessionmaker(bind=self.engine)

    def generate_dates(self, weekday=4):
        """Helper to generate every given weekday between start_year and end_year
        :param start_year: Year to begin counting. Inclusive
        :param end_year: Year to end counting. Inclusive
        :param weekday: Default 4 = Friday. Weekdays indexed from 0"""

        start_date = date(self.start_year, 1, 1)
        end_date = date(self.end_year, 12, 31)
        delta = end_date - start_date

        for day in range(delta.days + 1):
            new_date = start_date + timedelta(day)
            if isinstance(weekday, int):
                if new_date.weekday() == weekday:
                    delta_day = new_date
                else:
                    continue

            elif isinstance(weekday, list):
                if new_date.weekday() in weekday:
                    delta_day = new_date
                else:
                    continue
            elif weekday is None:
                delta_day = new_date
            else:
                raise TypeError("Weekday must be one of list, int or None")

            yield delta_day

    def insert_dates_between_years(self, **kwargs):
        session = self.session()
        for given_date in self.generate_dates(**kwargs):
            if not session.query(Morgenmad).filter_by(dato=given_date).first():
                morgenmad = Morgenmad(dato=given_date)
                session.add(morgenmad)
        session.commit()

    def users_per_breakfast(self):
        session = self.session()
        unassigned_breakfast = session.query(Morgenmad).filter(Morgenmad.user == None).all()
        all_users = session.query(User).order_by(User.id).all()
        for breakfast, user in zip(unassigned_breakfast, cycle(all_users)):
            breakfast.user = user
            session.add(breakfast)
        session.commit()

    def seed_db(self):
        users_json = pathlib.Path(BaseConfig.ROOT_DIR).joinpath('seed_users.json')
        seed_users(users_json)
        self.insert_dates_between_years()
        self.users_per_breakfast()




def seed_users(users_json):
    engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
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
