from itsdangerous import URLSafeTimedSerializer
from app.config import BaseConfig
from flask_mail import Message
from app.extensions import mail, db
from app.model import Morgenmad, User
from datetime import date, timedelta
from itertools import cycle


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


def generate_dates(start_year, end_year, weekday=4):
    """Helper to generate every given weekday between start_year and end_year
    :param start_year: Year to begin counting. Inclusive
    :param end_year: Year to end counting. Inclusive
    :param weekday: Default 4 = Friday. Weekdays indexed from 0"""

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


def insert_dates_into_morgenmad(start_year, end_year, **kwargs):
    users = User.query.order_by(User.list_order).all()
    for friday, user in zip(generate_dates(start_year, end_year, **kwargs), cycle(users)):
        morgenmad = Morgenmad(dato=friday)
        user.morgenmad.append(morgenmad)
        db.session.add(user)
    db.session.commit()
