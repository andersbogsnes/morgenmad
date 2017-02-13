from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from morgenmad.user.model import User, Morgenmad
from morgenmad.config import BaseConfig

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()


result = session.query(Morgenmad).filter(Morgenmad.is_next).first()

print([user.fullname for user in result.accepted_users])