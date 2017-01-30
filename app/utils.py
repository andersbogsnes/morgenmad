from itsdangerous import URLSafeTimedSerializer
from app.config import BaseConfig
from flask_mail import Message
from app.extensions import mail


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECRET_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECRET_SALT,
            max_age=expiration)
    except:
        return False
    return email

def send_confirmation_email(to, subject, template):
    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=BaseConfig.MAIL_DEFAULT_SENDER)
    mail.send(msg)
