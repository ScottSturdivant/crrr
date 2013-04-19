from crrr import db
from crrr.user import constants as USER

class Address(db.Model):
    """
    A table for storing physical addresses.
    """

    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.SmallInteger)
    line_1 = db.Column(db.String(), nullable=False)
    line_2 = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    zip = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=True)
    clinic = db.Column(db.String())
    vet_name = db.Column(db.String())

    # relations
    phones = db.relationship('Phone', lazy='dynamic')

    def __repr__(self):
        if self.line_2:
            addr = "%s %s %s, %s %s" % (self.line_1,
                                        self.line_2,
                                        self.city.capitalize(),
                                        self.state.upper(),
                                        self.zip)
        else:
            addr = "%s %s, %s %s" % (self.line_1,
                                     self.city.capitalize(),
                                     self.state.upper(),
                                     self.zip)

        return "<%s: %s>" % (self.getLocation().capitalize(), addr)

    def getLocation(self):
        return USER.LOCATIONS[self.location]
