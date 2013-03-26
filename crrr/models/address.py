from crrr import db

class AddressLocation(object):
    HOME = 'home'
    WORK = 'work'
    VET  = 'vet'


class Address(db.Model):
    """
    A table for storing physical addresses.
    """

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.Enum(AddressLocation.HOME,
                                 AddressLocation.WORK,
                                 AddressLocation.VET,
                                 name='name_location'))
    line_1 = db.Column(db.String(1024), nullable=False)
    line_2 = db.Column(db.String(1024), nullable=True)
    city = db.Column(db.String(1024), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(10), nullable=False)

