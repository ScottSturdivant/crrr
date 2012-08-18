from werkzeug.security import generate_password_hash, check_password_hash
from crrr import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    admin = db.Column(db.Boolean())
    active = db.Column(db.Boolean())

    def __init__(self, username, email, password="changeme", admin=False, active=True):
        self.username = username
        self.email = email
        self.set_password(password)
        self.admin = admin
        self.active = active

    def __repr__(self):
        return '<User %r: admin=%s>' % (self.username, self.admin)

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


class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    adopted = db.Column(db.Boolean())
    breed = db.Column(db.String(120))
    sex = db.Column(db.String(1))
    age = db.Column(db.String(120))
    mix = db.Column(db.Boolean())
    size = db.Column(db.String(120))
    fee = db.Column(db.Integer)
    description = db.Column(db.Text())
    special_needs = db.Column(db.Boolean())
    home_without_dogs = db.Column(db.Boolean())
    home_without_cats = db.Column(db.Boolean())
    home_without_kids = db.Column(db.Boolean())
    spayed = db.Column(db.Boolean())
    shots = db.Column(db.Boolean())
    housetrained = db.Column(db.Boolean())
    photo1_url = db.Column(db.String(120))
    photo2_url = db.Column(db.String(120))
    photo3_url = db.Column(db.String(120))
    archive = db.Column(db.Boolean())
    happy_tails = db.Column(db.Text())

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return '<Dog %r: adopted=%s>' % (self.name, self.adopted)

