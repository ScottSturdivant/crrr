from crrr import db
from crrr.user import constants as USER


class Phone(db.Model):
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))
    location = db.Column(db.SmallInteger)

    def __repr__(self):
        return "<%s Phone: %s>" % (self.getLocation().capitalize(), self.number)

    def __iszero__(self):
        return self.number

    def getLocation(self):
        return USER.PHONES[self.location]
