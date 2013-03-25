from werkzeug.security import generate_password_hash, check_password_hash
from crrr import db


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

