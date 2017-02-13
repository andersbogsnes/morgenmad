from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from morgenmad.user.model import User


class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired(message="Skal udfyldes"), Email(message="Ikke gyldig e-mail")])
    password = PasswordField('password', validators=[DataRequired(message="Skal udfyldes")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super().validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        if not self.user:
            self.email.errors.append('Ukendt Email')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Ugyldigt Passord")
            return False

        if not self.user.is_active:
            self.email.errors.append("Ikke aktiveret. Tjek din email!")
            return False
        return True