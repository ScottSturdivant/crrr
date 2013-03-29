from crrr import db

class Location(object):
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
    location = db.Column(db.Enum(Location.HOME,
                                 Location.WORK,
                                 Location.VET,
                                 name='name_location'))
    line_1 = db.Column(db.String(), nullable=False)
    line_2 = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    zip = db.Column(db.String(), nullable=False)
    duration = db.Column(db.String(), nullable=True)

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

        return "<%s: %s>" % (self.location.capitalize(), addr)
