from werkzeug.security import generate_password_hash, check_password_hash
from crrr import db


ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
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


class DogStatus(object):
    """
    Enum values for the dog model's status column.
    """
    ADOPTABLE = 'adoptable'
    ADOPTED   = 'adopted'
    HOLD      = 'hold'
    PENDING   = 'pending'


class DogAge(object):
    """
    Enum values for the dog model's age column.
    """
    PUPPY  = 'puppy'
    YOUNG  = 'young'
    ADULT  = 'adult'
    SENIOR = 'senior'


class DogSize(object):
    """
    Enum values for the dog model's size column.
    """
    SMALL  = 'small'
    MEDIUM = 'medium'
    LARGE  = 'large'
    XLARGE = 'x-large'


class Dog(db.Model):
    __tablename__ = 'dog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    status = db.Column(db.Enum(DogStatus.ADOPTABLE,
                               DogStatus.ADOPTED,
                               DogStatus.HOLD,
                               DogStatus.PENDING,
                               name='dog_status'))
    breed = db.Column(db.String(120))
    sex = db.Column(db.String(1))
    age = db.Column(db.Enum(DogAge.PUPPY,
                            DogAge.YOUNG,
                            DogAge.ADULT,
                            DogAge.SENIOR,
                            name='dog_age'))
    mix = db.Column(db.Boolean())
    size = db.Column(db.Enum(DogSize.SMALL,
                             DogSize.MEDIUM,
                             DogSize.LARGE,
                             DogSize.XLARGE))
    fee = db.Column(db.Integer)
    description = db.Column(db.Text())
    special_needs = db.Column(db.Boolean())
    home_without_dogs = db.Column(db.Boolean())
    home_without_cats = db.Column(db.Boolean())
    home_without_kids = db.Column(db.Boolean())
    spayed = db.Column(db.Boolean())
    shots = db.Column(db.Boolean())
    housetrained = db.Column(db.Boolean())
    archive = db.Column(db.Boolean())
    happy_tails = db.Column(db.Text())

    # relations
    pictures = db.relationship('Picture', lazy='dynamic')

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return '<Dog %r: adopted=%s>' % (self.name, self.adopted)


class Picture(db.model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'))
    title = db.Column(db.String(1024), nullable=False, index=True)
    file_url = db.Column(db.String(1024), nullable=False)
    thumb_url = db.Column(db.String(1024), nullable=False)

    def __init__(self, title):
        self.title = tile

    def __repr__(self):
        return "<Picture %s>" % (self.title)

