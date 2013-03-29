from crrr import db
from datetime import datetime

class Status(object):
    NEW          = 'new'
    INIT         = 'initial contact made'
    ARRANGE_HC   = 'arranging hc'
    HC_COMPLETED = 'hc completed'
    APPROVED     = 'approved'
    UNAPPROVED   = 'unapproved'


class App(db.Model):
    __tablename__ = 'app'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'))
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submittal_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum(Status.NEW,
                               Status.INIT,
                               Status.ARRANGE_HC,
                               Status.HC_COMPLETED,
                               Status.APPROVED,
                               Status.UNAPPROVED,
                               name='app_status'),
                               default=Status.NEW)
    archive = db.Column(db.Boolean, default=False)

    # relationships
    applicant = db.relationship('User', foreign_keys=[user_id], backref='apps')
    assignee  = db.relationship('User', foreign_keys=[assignee_id])
    dog = db.relationship('Dog', backref='apps')

