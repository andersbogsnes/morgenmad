from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import User, Morgenmad
from app.config import BaseConfig

engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()

result = session.query(User).get(2)
next_morgenmad = session.query(Morgenmad).filter(Morgenmad.is_next).first()
next_morgenmad.accepted_users.append(result)
session.add(next_morgenmad)
session.commit()

result = session.query(Morgenmad).filter(Morgenmad.is_next).first()

print(result.accepted_users)