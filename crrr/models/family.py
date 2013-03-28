from crrr import db

class FamilyRelations(object):
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
    relation = db.Column(db.Enum(FamilyRelations.NA,
                                 FamilyRelations.SPOUSE,
                                 FamilyRelations.PARTNER,
                                 FamilyRelations.BROTHER,
                                 FamilyRelations.SISTER,
                                 FamilyRelations.SON,
                                 FamilyRelations.DAUGHTER,
                                 FamilyRelations.FRIEND,
                                 FamilyRelations.OTHER,
                                 name='family_relations'))
    name = db.Column(db.String())
    age = db.Column(db.String(), nullable=True)

    def __init__(self, name, relation, user_id, age=None):
        self.name = name
        self.relation = relation
        self.user_id = user_id
        self.age = age

    def __repr__(self):
        return "<Family: %s is a %s>" % (self.name, self.relation)
