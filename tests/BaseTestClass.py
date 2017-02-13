from flask_testing import TestCase
from morgenmad.app import create_app
from morgenmad.config import TestConfig
from morgenmad.extensions import db


class BaseTestClass(TestCase):
    """Base class for testing"""

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        self.user = dict(fornavn="Testy", efternavn="Mctesterson", email="test@testing.com", tlf_nr="12345678",
                         password="secret")
        self.user_response = dict(id=1, fullname="Testy Mctesterson", email="test@testing.com")
        self.user_after_update = dict(fornavn="Testy", efternavn="Changed", email="test@testing.com", tlf_nr="12345678",
                                      password="secret")

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_env(self):
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['WTF_CSRF_ENABLED'])