from crrr import db


class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    email = db.Column(db.String(), nullable=False)

    foster_fam = db.Column(db.Boolean)
    transport = db.Column(db.Boolean)
    home_check = db.Column(db.Boolean)
    ref_check = db.Column(db.Boolean)
    crate = db.Column(db.Boolean)
    supplies = db.Column(db.Boolean)

    # relationships
    phones = db.relationship('Phone')
