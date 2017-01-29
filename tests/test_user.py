from app.model import User
import pytest


def test_User_model(session):
    user = User(fornavn="Test",
                efternavn="Mctesterson",
                tlf_nr="22163821",
                email="test@testing.com",
                password="password")
    session.add(user)
    session.commit()

    assert user.id > 0
