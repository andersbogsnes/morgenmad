from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import User, Morgenmad
from app.config import BaseConfig
import datetime
from itertools import cycle

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# results = session.query(User).filter_by(email='andersbogsnes@gmail.com').all()

def add_dates_and_users():
    year = 2017
    end_year = 2019

    startdate = datetime.date(year, 1, 1)
    enddate = datetime.date(end_year, 12, 31)

    delta = enddate - startdate

    for day in range(delta.days + 1):
        newdate = startdate + datetime.timedelta(day)
        if newdate.weekday() == 4:
            morgenmad = Morgenmad(dato=newdate)
            session.add(morgenmad)

    session.commit()

    order = [user for user in session.query(User).order_by(User.list_order)]

    for friday, user in zip(session.query(Morgenmad).all(), cycle(order)):
        user.morgenmad.append(friday)
        session.add(user)
    session.commit()

fridays = session.query(Morgenmad).all()

for friday in fridays:
    print(friday.user.fullname)

