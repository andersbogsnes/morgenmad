from morgenmad.extensions import db, bcrypt, ma
from flask_login import UserMixin
from marshmallow import fields

morgenmad_users_table = db.Table('morgenmad_users',
                                 db.Column('morgenmad_id', db.Integer, db.ForeignKey('morgenmad.id')),
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fornavn = db.Column(db.String(250))
    efternavn = db.Column(db.String(250))
    tlf_nr = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.LargeBinary(128), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    tlf_nr_confirmed = db.Column(db.Boolean, default=False)
    morgenmad = db.relationship('Morgenmad', backref='user')
    created_on = db.Column(db.DateTime, default=db.func.now())
    last_modified = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, fornavn, efternavn, tlf_nr, email, password):
        self.fornavn = fornavn
        self.efternavn = efternavn
        self.tlf_nr = tlf_nr
        self.email = email
        self.set_password(password)

    @property
    def fullname(self):
        return f"{self.fornavn} {self.efternavn}"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.fullname}>"


class Morgenmad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dato = db.Column(db.Date, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_next = db.Column(db.Boolean, default=False)
    accepted_users = db.relationship('User',
                                     secondary=morgenmad_users_table,
                                     backref=db.backref('accepteret'))


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

    email = fields.Email()
