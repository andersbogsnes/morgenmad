from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class SignupForm(FlaskForm):
    firstname = StringField('firstname', validators=[DataRequired(message="Skal udfyldes")])
    lastname = StringField('lastname', validators=[DataRequired(message="Skal udfyldes")])
    email = StringField('email', validators=[DataRequired(message="Skal udfyldes"),
                                             Email(message="Ikke gyldig e-mail")])
    password = PasswordField('password', validators=[DataRequired(message="Skal udfyldes")])
    confirm = PasswordField('confirm', validators=[DataRequired(message="Skal udfyldes"),
                                                   EqualTo('password',
                                                           message="Passordene skal være ens")])
    tlf_nr = StringField('telefon', validators=[DataRequired(message="Skal udfyldes")])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message="Skal udfyldes"), Email(message="Ikke gyldig e-mail")])
    password = PasswordField('password', validators=[DataRequired(message="Skal udfyldes")])
