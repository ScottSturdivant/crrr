from werkzeug.security import generate_password_hash, check_password_hash
from crrr import db
from crrr.dogs import constants as DOG

class Dog(db.Model):
    __tablename__ = 'dog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.SmallInteger)
    breed = db.Column(db.String())
    sex = db.Column(db.SmallInteger)
    age = db.Column(db.SmallInteger)
    mix = db.Column(db.Boolean())
    size = db.Column(db.SmallInteger)
    fee = db.Column(db.Integer)
    description = db.Column(db.Text())
    special_needs = db.Column(db.Boolean())
    home_without_dogs = db.Column(db.Boolean())
    home_without_cats = db.Column(db.Boolean())
    home_without_kids = db.Column(db.Boolean())
    fixed = db.Column(db.Boolean())
    shots = db.Column(db.Boolean())
    housetrained = db.Column(db.Boolean())
    archive = db.Column(db.Boolean(), default=False)
    happy_tails = db.Column(db.Text())

    # relations
    pictures = db.relationship('Picture')

    def __repr__(self):
        return '<Dog %r: adopted=%s>' % (self.name, self.getStatus())

    def getStatus(self):
        return DOG.STATUS[self.status]

    def setStatus(self, status):
        self.status = [k for k,v in DOG.STATUS.items() if v==status][0]

    def getSex(self):
        return DOG.SEX[self.sex]

    def setSex(self, sex):
        self.sex = [k for k,v in DOG.SEX.items() if v==sex][0]

    def getSize(self):
        return DOG.SIZE[self.size]

    def setSize(self, size):
        self.size = [k for k,v in DOG.SIZE.items() if v==size][0]
    def getAge(self):
        return DOG.AGE[self.age]
