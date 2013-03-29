from crrr import db

class Relations(object):
    NA = 'N/A'
    SPOUSE = 'spouse'
    PARTNER = 'partner'
    BROTHER = 'brother'
    SISTER = 'sister'
    SON = 'son'
    DAUGHTER = 'daughter'
    FRIEND = 'friend'
    OTHER = 'other'


class Family(db.Model):
    __tablename__ = 'family'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relation = db.Column(db.Enum(Relations.NA,
                                 Relations.SPOUSE,
                                 Relations.PARTNER,
                                 Relations.BROTHER,
                                 Relations.SISTER,
                                 Relations.SON,
                                 Relations.DAUGHTER,
                                 Relations.FRIEND,
                                 Relations.OTHER,
                                 name='family_relations'))
    name = db.Column(db.String())
    age = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return "<Family: %s is a %s>" % (self.name, self.relation)

    def __nonzero__(self):
        return False if self.relation == Relations.NA else True
