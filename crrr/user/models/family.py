from crrr import db
from crrr.user import constants as USER

class Family(db.Model):
    __tablename__ = 'family'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relation = db.Column(db.SmallInteger)
    name = db.Column(db.String())
    age = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return "<Family: %s is a %s>" % (self.name, self.getRelation())

    def __nonzero__(self):
        return False if self.relation else True

    def getRelation(self):
        return USER.RELATIONSHIPS[self.relation]
