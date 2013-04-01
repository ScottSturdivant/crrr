from crrr import db


class Confirm(db.Model):
    """
    A table to hold user confirmation hashes.

    To be used when a user registers, an email will be sent to their account
    which they click on, taking them to a page that allows them to confirm
    their account and be signed in.
    """
    __tablename__ = 'confirm'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hash = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Confirm user id: %d, hash=%s>" % (self.user_id, self.hash)
