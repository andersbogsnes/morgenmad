from flask import url_for
from flask_login import current_user

from morgenmad.extensions import db
from morgenmad.user.model import User
from tests.BaseTestClass import BaseTestClass


class TestUserViews(BaseTestClass):
    def test_login_page(self):
        response = self.client.get('/login')
        self.assert200(response)
        self.assert_template_used('public/login.html')
        self.assertTrue(b'<h1 class="title">Login</h1>' in response.data)

    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assert200(response)
        self.assert_template_used('public/signup.html')
        self.assertTrue(b'<h1 class="title">Registrer</h1>' in response.data)

    def test_signup_function(self):
        new_user = dict(firstname='Test',
                        lastname='Mctesterson',
                        email='test@mctest.com',
                        password='password',
                        confirm='password',
                        tlf_nr='123456')
        with self.client:
            response = self.client.post('/signup', data=new_user)
            self.assert_redirects(response, url_for('public.main'))

            user = User.query.filter_by(email=new_user['email']).one()
            self.assertTrue(user.fornavn == new_user['firstname'])

    def test_login_function_email_validated(self):
        new_user = User(**self.user)
        new_user.email_confirmed = True
        db.session.add(new_user)
        db.session.commit()

        with self.client:
            response = self.client.post('/login', data={"email": self.user['email'],
                                                            "password": self.user['password']})
            self.assert_redirects(response, url_for('user.profile'))
            self.assertTrue(current_user.email == self.user['email'])
            self.assertFalse(current_user.is_anonymous)

    def test_login_function_email_not_validated(self):
        new_user = User(**self.user)
        db.session.add(new_user)
        db.session.commit()

        response = self.client.post('/login',
                                    data={"email": self.user['email'],
                                          "password": self.user['password']}
                                    )
        self.assert_redirects(response, url_for('user.profile'))

    def test_non_existant_login(self):
        response = self.client.post('/login',
                                    data={"email": self.user['email'],
                                          "password": self.user['password']},
                                    follow_redirects=True)
        self.assertTrue(b"Ukendt Email" in response.data)
