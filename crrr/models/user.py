from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from crrr import db


ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    # relations
    addresses = db.relationship('Address', lazy='dynamic')
    pets = db.relationship('Pet', lazy='dynamic')
    relations = db.relationship('Family', lazy='dynamic')
    employment = db.relationship('Employment', lazy='dynamic')
    phones = db.relationship('Phone', lazy='dynamic')
    profile = db.relationship('Profile', uselist=False)

    def __repr__(self):
        role = 'Admin' if self.role else 'User'
        return '<User %s: role=%s>' % (self.username, role)

    def is_active(self):
        return self.active

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return unicode(self.id)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
