from crrr import db
from datetime import datetime


class Reset(db.Model):
    """
    A table to hold user password reset requests.
    """
    __tablename__ = 'reset'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hash = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Reset user id: %s, hash=%s, timestamp=%s>" % (self.user_id, self.hash, self.timestamp)
