from flask import url_for
from tests.BaseTestClass import BaseTestClass
from app.extensions import db
from app.model import User
from flask_login import current_user


class TestUserViews(BaseTestClass):
    def test_login_page(self):
        response = self.client.get('user/login')
        self.assert200(response)
        self.assert_template_used('login.html')
        self.assertTrue(b'<h1 class="title">Login</h1>' in response.data)

    def test_signup_page(self):
        response = self.client.get('user/signup')
        self.assert200(response)
        self.assert_template_used('signup.html')
        self.assertTrue(b'<h1 class="title">Registrer</h1>' in response.data)

    def test_signup_function(self):
        new_user = dict(firstname='Test',
                        lastname='Mctesterson',
                        email='test@mctest.com',
                        password='password',
                        confirm='password',
                        tlf_nr='123456')

        response = self.client.post('user/signup', data=new_user)
        self.assert_redirects(response, url_for('user.profile'))

        user = User.query.filter_by(email=new_user['email']).one()
        self.assertTrue(user.fornavn == new_user['firstname'])

    def test_login_function_email_validated(self):
        new_user = User(**self.user)
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()

        with self.client:
            response = self.client.post('user/login', data={"email": self.user['email'],
                                                            "password": self.user['password']})
            self.assert_redirects(response, url_for('user.profile'))
            self.assertTrue(current_user.email == self.user['email'])
            self.assertFalse(current_user.is_anonymous)

    def test_login_function_email_not_validated(self):
        new_user = User(**self.user)
        db.session.add(new_user)
        db.session.commit()

        response = self.client.post('user/login',
                                    data={"email": self.user['email'],
                                          "password": self.user['password']}
                                    )
        self.assert_redirects(response, url_for('main.main'))

    def test_non_existant_login(self):
        response = self.client.post('user/login',
                                    data={"email": self.user['email'],
                                          "password": self.user['password']},
                                    follow_redirects=True)
        self.assertTrue(b"Forkert bruger og/eller passord" in response.data)
