from crrr import db
from crrr.user import constants as USER


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    free_feed = db.Column(db.Boolean)
    who_cares = db.Column(db.String())
    home = db.Column(db.String())
    needs = db.Column(db.Text)
    alone_time = db.Column(db.String())
    dog_kept_home = db.Column(db.String())
    dog_kept_away = db.Column(db.String())
    dog_door = db.Column(db.String())
    transport = db.Column(db.String())
    crate = db.Column(db.String())
    sleep = db.Column(db.String())
    why_ridgebacks = db.Column(db.String())
    before_pets = db.Column(db.Text)
    expenses = db.Column(db.String())
    day_in_the_life = db.Column(db.Text)
    dog_as_family = db.Column(db.Text)
    activity_level = db.Column(db.Text)
    away_care = db.Column(db.Text)
    give_up = db.Column(db.Text)
    housing = db.Column(db.SmallInteger)
    own_rent = db.Column(db.SmallInteger)
    landlord_proof = db.Column(db.SmallInteger)
    yard = db.Column(db.Boolean)
    fence = db.Column(db.Boolean)
    fence_details = db.Column(db.Text)
    ridgeback_gender = db.Column(db.SmallInteger)
    ridgeback_age = db.Column(db.String())
    ridgeback_ridges = db.Column(db.SmallInteger)
    ridgeback_purebred = db.Column(db.SmallInteger)
    ridgeback_health_problems = db.Column(db.String())
    ridgeback_social_problems = db.Column(db.String())
                                       
    def getHousing(self):
        return USER.HOME_TYPES[self.housing]

    def getOwnRent(self):
        return USER.OWNERSHIP[self.own_rent]

    def getLandlordProof(self):
        return USER.LANDLORD_PROOF[self.landlord_proof]

    def getRidgebackGender(self):
        return USER.GENDER_PREFERENCE[self.ridgeback_gender]

    def getRidgebackRidges(self):
        return USER.RIDGED_PREFERENCE[self.ridgeback_ridges]

    def getRidgebackPurebred(self):
        return USER.PUREBRED_PREFERENCE[self.ridgeback_purebred]

