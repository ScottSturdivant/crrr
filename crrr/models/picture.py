from werkzeug.security import generate_password_hash, check_password_hash
from crrr import db

class Picture(db.Model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'))
    title = db.Column(db.String(), nullable=False, index=True)
    file_url = db.Column(db.String(), nullable=False)
    thumb_url = db.Column(db.String(), nullable=False)

    def __init__(self, title):
        self.title = tile

    def __repr__(self):
        return "<Picture %s>" % (self.title)

