from crrr import db
from crrr.user import constants as USER



class Employment(db.Model):
    __tablename__ = 'employment'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(), nullable = False)
    occupation = db.Column(db.String(), nullable = True)
    status = db.Column(db.SmallInteger)

    def __repr__(self):
        return "<Employment: %s @ %s>" % (self.getStatus(), self.name)

    def getStatus(self):
        return USER.EMPLOYMENT_STATUS[self.status]
