from app.extensions import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tlf_nr = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean)
    tlf_nr_confirmed = db.Column(db.Boolean)
    morgenmad = db.relationship('Morgenmad', backref='user')

    def __init__(self, tlf_nr, email, password):
        self.tlf_nr = tlf_nr
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Morgenmad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dato = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))