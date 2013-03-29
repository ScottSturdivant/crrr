from crrr import db

locations = [
    'house',
    'garage',
    'basement'
    'laundry room',
    'yard',
    'outdoor kennel',
    'tie out',
    'crate',
    'dog run',
    'other'
    ]

reasons = [
    'companion',
    'guard dog',
    'gift',
    'breeding',
    'protection',
    'competition',
    'agility',
    'lure coursing',
    'obedience',
    'other',
    ]

housing = ['house','townhome','apartment','condo',
           'mobile home','ranch','farm','duplex','other']

ownership = ['own', 'rent']

proof = ['yes', 'no', 'n/a']

yes_no = ['yes', 'no']


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    free_feed = db.Column(db.Boolean)
    who_cares = db.Column(db.String())
    home = db.Column(db.String())
    needs = db.Column(db.Text)
    alone_time = db.Column(db.String())
    dog_kept_home = db.Column(db.Enum(*locations,
                                      name='profile_dog_kept_home'))
    dog_kept_away = db.Column(db.Enum(*locations,
                                      name='profile_dog_kept_away'))
    dog_door = db.Column(db.String())
    transport = db.Column(db.String())
    crate = db.Column(db.String())
    sleep = db.Column(db.String())
    why_ridgebacks = db.Column(db.Enum(*reasons,
                                       name='profile_why_ridgebacks'))
    before_pets = db.Column(db.Text)
    expenses = db.Column(db.String())
    day_in_the_life = db.Column(db.Text)
    dog_as_family = db.Column(db.Text)
    activity_level = db.Column(db.Text)
    away_care = db.Column(db.Text)
    give_up = db.Column(db.Text)
    housing = db.Column(db.Enum(*housing, name='profile_housing'))
    own_rent = db.Column(db.Enum(*ownership, name='profile_own_rent'))
    landlord_proof = db.Column(db.Enum(*proof,
                                       name='profile_landlord_proof'))
    yard = db.Column(db.Enum(*yes_no,
                             name='profile_yard'))
    fence = db.Column(db.Enum(*yes_no,
                              name='profile_fence'))
    fence_details = db.Column(db.Text)

