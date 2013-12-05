from crrr import db

class Status(object):
    FULL = 'full time'
    PART = 'part time'
    NONE = 'unemployed'


class Employment(db.Model):
    __tablename__ = 'employment'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(), nullable = False)
    occupation = db.Column(db.String(), nullable = True)
    status = db.Column(db.Enum(Status.FULL,
                               Status.PART,
                               Status.NONE,
                               name='employment_status'))

    def __repr__(self):
        return "<Employment: %s @ %s>" % (self.status, self.name)
