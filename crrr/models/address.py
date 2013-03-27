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
    line_1 = db.Column(db.String(), nullable=False)
    line_2 = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    zip = db.Column(db.String(), nullable=False)

