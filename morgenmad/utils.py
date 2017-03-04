from itsdangerous import URLSafeTimedSerializer
from morgenmad.config import BaseConfig
from flask_mail import Message
from morgenmad.extensions import mail, db
from morgenmad.user.model import Morgenmad, User
from datetime import date, timedelta
from itertools import cycle
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


def generate_dates(start_year=None, end_year=None, weekday=4):
    """Helper to generate every given weekday between start_year and end_year
    """
    start_year = start_year or date.today().year
    end_year = end_year or date.today().year + 1

    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
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


def insert_dates_between_years(start_year=None, end_year=None, weekday=4):
    """Inserts all dates generated in the interval"""
    for given_date in generate_dates(start_year, end_year, weekday):
        if not db.session.query(Morgenmad).filter_by(dato=given_date).first():
            morgenmad = Morgenmad(dato=given_date)
            db.session.add(morgenmad)
        db.session.commit()


def users_per_breakfast():
    unassigned_breakfast = db.session.query(Morgenmad).filter(Morgenmad.user == None).all()
    all_users = db.session.query(User).order_by(User.id).all()
    for breakfast, user in zip(unassigned_breakfast, cycle(all_users)):
        breakfast.user = user
        db.session.add(breakfast)
    db.session.commit()


def set_active_morgenmad(self):
    with self.app.app_context():
        last_breakfast = db.session.query(Morgenmad).filter(Morgenmad.is_next).first()
        if last_breakfast:
            last_breakfast.is_next = False
            db.session.add(last_breakfast)
        next_breakfast = db.session.query(Morgenmad).filter(Morgenmad.dato == next_friday()).first()
        next_breakfast.is_next = True
        db.session.add(next_breakfast)
        db.session.commit()

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
