from crrr import db

class Types(object):
    HOME = 'home'
    WORK = 'work'
    CELL = 'cell'


class Phone(db.Model):
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    location = db.Column(db.Enum(Types.HOME,
                                 Types.WORK,
                                 Types.CELL,
                                 name='phone_location'))

    def __repr__(self):
        if self.location:
            return "<%s Phone: %s>" % (self.location.capitalize(), self.number)
        else:
            return "<Phone id: %s>" % self.id

    def __iszero__(self):
        return self.number
