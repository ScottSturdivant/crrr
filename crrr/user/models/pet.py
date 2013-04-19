from crrr import db
from crrr.dogs import constants as DOGS


class Pet(db.Model):

    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    type = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    gender = db.Column(db.SmallInteger(), nullable=False)
    age = db.Column(db.String())
    altered = db.Column(db.Boolean, nullable=False)
    whathappened = db.Column(db.Text)

    def __repr__(self):
        return "<Pet: %s>" % (self.name)

    def getGender(self):
        return DOGS.SEX[self.gender]
