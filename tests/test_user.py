from flask_testing import TestCase
from flask import url_for
from app.morgenmad import create_app
from app.extensions import db
from app.config import TestConfig
from app.model import User
import json
from sqlalchemy.orm.exc import NoResultFound


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


class UserApiTest(BaseTestClass):

    def test_get_no_users(self):
        response = self.client.get(url_for('user_api.user_view'))
        self.assertEqual(response.json, [])

    def test_get_test_user(self):
        user = User(**self.user)
        db.session.add(user)
        db.session.commit()

        response = self.client.get(url_for('user_api.user_view'))
        self.assertTrue(isinstance(response.json, list))
        self.assertEqual(response.json, [self.user_response])

    def test_get_user_by_id(self):
        user = User(**self.user)
        db.session.add(user)
        db.session.commit()

        response = self.client.get(url_for('user_api.user_view', user_id=1))
        self.assertEqual(response.json, self.user_response)

    def test_get_non_existant_user_by_id(self):
        response = self.client.get(url_for('user_api.user_view', user_id=2))
        self.assertEqual(response.json, dict(error="404: Not Found"))

    def test_create_new_user(self):
        response = self.client.post(url_for('user_api.user_view'),
                                    data=json.dumps(self.user),
                                    content_type='application/json')
        self.assert200(response)

        response = self.client.get(url_for('user_api.user_view'))
        self.assertEqual(response.json, [self.user_response])

    def test_updating_existing_user(self):
        user = User(**self.user)
        db.session.add(user)
        db.session.commit()

        response = self.client.put(url_for('user_api.user_view', user_id=user.id),
                                   data=json.dumps({'efternavn': 'Changed'}),
                                   content_type='application/json')
        self.assert_status(response, 201)
        self.assertEqual(response.json, dict(success="User updated"))
        result = User.query.filter_by(id=user.id).one()
        self.assertEqual(result.efternavn, self.user_after_update['efternavn'])

    def test_updating_non_existing_user(self):
        response = self.client.put(url_for('user_api.user_view', user_id=1),
                                   data=json.dumps({'efternavn': 'Changed'}),
                                   content_type='application/json')
        self.assert404(response)
        self.assertEqual(response.json, dict(error="User not found"))
        self.assertRaises(NoResultFound, User.query.filter_by(id=1).one)
