from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from morgenmad.user.model import User

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super().validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email findes allerede")
            return False
        return True
