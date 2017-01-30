from app.extensions import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fornavn = db.Column(db.String(250))
    efternavn = db.Column(db.String(250))
    tlf_nr = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean)
    tlf_nr_confirmed = db.Column(db.Boolean)
    morgenmad = db.relationship('Morgenmad', backref='user')

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
    @property
    def is_active(self):
        return True

    @property
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class Morgenmad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dato = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
