from crrr.states import STATES
from crrr.admin.models import User
from flask.ext.wtf import Form
from wtforms import (
    TextField,
    SelectField,
    BooleanField,
    PasswordField,
    SubmitField,
    SelectMultipleField,
    validators
)


class Email(Form):
    email = TextField('Email', [validators.Email("This doesn't appear to be a valid email address."),
                                validators.Required('An email address is required.')])
    send = SubmitField('Send')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user is None:
            self.email.errors.append('Sorry, we have no record for this email address.')
            return False

        self.user = user
        return True


class ResetPassword(Form):
    password = PasswordField('Password', [validators.Required("You're goign to need a password."),
                                          validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')
    reset = SubmitField('Reset')


class CreateUser(Form):
    username = TextField("User Name", [validators.Required('A username is required.')])
    email = TextField('Email', [validators.Email("This doesn't appear to be a valid email address."),
                                validators.Required('An email address is required.')])
    password = PasswordField('Password', [validators.Required("You're going to need a password."),
                                          validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')
    register = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.username == self.username.data).first()
        if user:
            self.username.errors.append('This username is already taken.')
            return False

        user = User.query.filter(User.email == self.email.data).first()
        if user:
            self.email.errors.append('This email address is already in use.')
            return False

        self.user = user
        return True


class Address(Form):
    addr_1 = TextField("Address Line 1", [validators.Length(min=1, max=128), validators.Required()])
    addr_2 = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    city = TextField("City", [validators.Length(min=1, max=128), validators.Required()])
    state = SelectField("State", [validators.Required()], choices=sorted(zip(STATES, STATES)), default="CO")
    zip_code = TextField("Zip Code", [validators.Required(), validators.Regexp('^(\d{5}(-\d{4})?)?$')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(Address, self).__init__(*args, **kwargs)


class PersonalInfo(Address):
    first_name = TextField("First Name", [validators.Length(min=1, max=25), validators.Required()])
    last_name = TextField("Last Name", [validators.Length(min=1, max=35), validators.Required()])
    email = TextField("Email", [validators.Email(), validators.Required()])
    phone_h = TextField("Phone (h)",
                        [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_c = TextField("Phone (c)",
                        [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_w = TextField("Phone (w)",
                        [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(PersonalInfo, self).__init__(*args, **kwargs)

    def __iter__(self):
        """Re-order the way the fields are rendered."""
        vals = ['first_name', 'last_name', 'addr_1', 'addr_2', 'city', 'state', 'zip_code',
                'email', 'phone_h', 'phone_c', 'phone_w', 'csrf_token']
        for val in vals:
            yield getattr(self, val)


class Volunteer(PersonalInfo):
    foster = BooleanField(label='Be a foster family for a rescued Ridgeback.')
    transport = BooleanField(label=('Help transport a rescue dog.  For example, '
                                    'to and from a vet appointment or from a '
                                    'surrenduring situation to foster care.'))
    home_check = BooleanField(label='Help with home checks for a prospective adopter.')
    adopter_check = BooleanField(label=('Help with reference checks for a prospective '
                                        'adopter.  This requires telephone time.'))
    donate_crate = BooleanField(label='Donate a large dog crate.')
    donate_supplies = BooleanField(label='Buy food or dog supplies such as beds, leashes, collars, etc.')
    other = BooleanField(label='Other')
    other_input = TextField(label='OtherInput')

    submit = SubmitField('Volunteer')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(Volunteer, self).__init__(*args, **kwargs)

    def __iter__(self):
        """Re-order the way the fields are rendered."""
        vals = ['first_name', 'last_name', 'addr_1', 'addr_2', 'city', 'state', 'zip_code',
                'email', 'phone_h', 'phone_c', 'phone_w', 'foster', 'transport', 'home_check',
                'adopter_check', 'donate_crate', 'donate_supplies', 'other', 'other_input', 'csrf_token']
        for val in vals:
            yield getattr(self, val)


class Login(Form):
    username = TextField("Username", [validators.Length(max=12)])
    password = PasswordField("Password", [validators.Required()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.login_errors = []

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.username == self.username.data).first()
        if user is None:
            self.login_errors.append('Login failed.')
            return False

        if not user.check_password(self.password.data):
            self.login_errors.append('Login failed.')
            return False

        if not user.active:
            self.login_errors.append('This account is inactive.')
            return False

        return True


class Application(PersonalInfo):
    address_length = TextField("How long have you lived at this address?", [validators.Optional()])
    # Employer
    employer = TextField("Employer Name", [validators.Length(min=1, max=128)])
    occupation = TextField("Occupation", [validators.Optional()])
    choices = ['full time', 'part time', 'unemployed']
    employment_type = SelectField("Employment Status", [validators.Required()],
                                  choices=[(val, val.capitalize()) for val in choices])
    # Family
    choices = ['N/A', 'spouse', 'partner', 'brother', 'sister', 'son', 'daughter', 'friend', 'other']
    relation1 = SelectField("Relation", choices=[(val, val[0].upper() + val[1:]) for val in choices])
    name1 = TextField("Name", [validators.Optional(), validators.Length(max=128)])
    relation2 = SelectField("Relation", choices=[(val, val[0].upper() + val[1:]) for val in choices])
    name2 = TextField("Name", [validators.Optional(), validators.Length(max=128)])
    relation3 = SelectField("Relation", choices=[(val, val[0].upper() + val[1:]) for val in choices])
    name3 = TextField("Name", [validators.Optional(), validators.Length(max=128)])
    relation4 = SelectField("Relation", choices=[(val, val[0].upper() + val[1:]) for val in choices])
    name4 = TextField("Name", [validators.Optional(), validators.Length(max=128)])
    relation5 = SelectField("Relation", choices=[(val, val[0].upper() + val[1:]) for val in choices])
    name5 = TextField("Name", [validators.Optional(), validators.Length(max=128)])
    kids = TextField("If you have kids, what are their ages and names?",
                     [validators.Optional(), validators.Length(max=256)])
    # Vet
    ref1_firstname = TextField("Clinic Name", [validators.Required(), validators.Length(min=1, max=128)])
    ref1_lastname = TextField("Veterinarian's Name", [validators.Required(), validators.Length(min=1, max=128)])
    ref1_address1 = TextField("Address Line 1", [validators.Required(), validators.Length(min=1, max=128)])
    ref1_address2 = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    ref1_city = TextField("City", [validators.Required(), validators.Length(min=1, max=128)])
    ref1_state = SelectField("State", [validators.Required()], choices=sorted(zip(STATES, STATES)), default="CO")
    ref1_zip = TextField("Zip Code", [validators.Required(), validators.Regexp('^(\d{5}(-\d{4})?)?$')])
    ref1_phone = TextField("Phone", [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    # Pet
    pet_1_species = TextField("Pet Type", description="Dog / Card / Bird / etc")
    pet_1_sex = SelectField("Pet Sex", choices=[('m', 'M'), ('f', 'F')])
    pet_1_age = TextField("Pet Age")
    pet_1_name = TextField("Pet Name")
    pet_1_altered = SelectField('Pet Altered', choices=[('n', 'N'), ('y', 'Y')])
    pet_1_whathappened = TextField("What Happened")
    pet_2_species = TextField("Pet Type", description="Dog / Card / Bird / etc")
    pet_2_sex = SelectField("Pet Sex", choices=[('m', 'M'), ('f', 'F')])
    pet_2_age = TextField("Pet Age")
    pet_2_name = TextField("Pet Name")
    pet_2_altered = SelectField('Pet Altered', choices=[('n', 'N'), ('y', 'Y')])
    pet_2_whathappened = TextField("What Happened")
    pet_3_species = TextField("Pet Type", description="Dog / Card / Bird / etc")
    pet_3_sex = SelectField("Pet Sex", choices=[('m', 'M'), ('f', 'F')])
    pet_3_age = TextField("Pet Age")
    pet_3_name = TextField("Pet Name")
    pet_3_altered = SelectField('Pet Altered', choices=[('n', 'N'), ('y', 'Y')])
    pet_3_whathappened = TextField("What Happened")
    pet_4_species = TextField("Pet Type", description="Dog / Card / Bird / etc")
    pet_4_sex = SelectField("Pet Sex", choices=[('m', 'M'), ('f', 'F')])
    pet_4_age = TextField("Pet Age")
    pet_4_name = TextField("Pet Name")
    pet_4_altered = SelectField('Pet Altered', choices=[('n', 'N'), ('y', 'Y')])
    pet_4_whathappened = TextField("What Happened")
    pet_5_species = TextField("Pet Type", description="Dog / Card / Bird / etc")
    pet_5_sex = SelectField("Pet Sex", choices=[('m', 'M'), ('f', 'F')])
    pet_5_age = TextField("Pet Age")
    pet_5_name = TextField("Pet Name")
    pet_5_altered = SelectField('Pet Altered', choices=[('n', 'N'), ('y', 'Y')])
    pet_5_whathappened = TextField("What Happened")
    # Pet Care
    freefeed = SelectField('Do you free feed your pets?', choices=[('n', 'N'), ('y', 'Y')],
                           validators=[validators.Required()])
    whocares = TextField('Who will be responsible for feeding, exercising, and training your rescued Ridgeback?',
                         [validators.Required(), validators.Length(min=1, max=256)])
    home = TextField('Is someone home during the day?', [validators.Required(), validators.Length(min=1, max=256)])
    needs = TextField('How will your rescued Ridgeback\'s exercise / potty needs be met if no one is home during the day?',
                      [validators.Required(), validators.Length(min=1, max=256)])
    alonetime = TextField('How many hours per day will your rescued Ridgeback be alone?',
                          [validators.Required(), validators.Length(min=1, max=256)])
    choices = ['house', 'garage', 'basement', 'laundry room', 'yard', 'outdoor kennel',
               'tie out', 'crate', 'dog run', 'other']
    dogkepthome = SelectMultipleField('When you are home, your rescued Ridgeback will be kept',
                                      [validators.Required()],
                                      choices=[(val, val.capitalize()) for val in choices])
    dogkeptaway = SelectMultipleField('When you are away, your rescued Ridgeback will be kept',
                                      [validators.Required()],
                                      choices=[(val, val.capitalize()) for val in choices])
    dogdoor = TextField('Do you have a dog door?  If so, where?',
                        [validators.Required(), validators.Length(min=1, max=256)])
    transport = TextField('How will you transport your rescued Ridgeback in your vehicle?',
                          [validators.Required(), validators.Length(min=1, max=256)])
    crate = TextField('Do you plan to use a crate for your rescued Ridgeback?  If so, when?',
                      [validators.Required(), validators.Length(min=1, max=256)])
    sleep = TextField('Where will the rescued Ridgeback sleep?',
                      [validators.Required(), validators.Length(min=1, max=256)])
    choices = ['companion', 'guard dog', 'gift', 'breeding', 'protection', 'competitions',
               '  - Agility', '  - Lure Coursing', '  - Obedience']
    whyridgebacks = SelectMultipleField('Why do you want to adopt a Ridgeback?  Select all that apply.',
                                        [validators.Required()],
                                        choices=[(val, val.capitalize()) for val in choices],
                                        description='Hold down CTRL to select multiple options.')
    before = TextField('Have you ever owned a Ridgeback before?',
                       [validators.Required(), validators.Length(min=1, max=256)])
    expenses = TextField('Beyond routine veterinary care, training classes, food and supplies for your rescued Ridgeback, are you prepared for expenses in case of accidents or major illnesses?',
                         [validators.Required(), validators.Length(min=1, max=256)])
    # A day in the life
    dayinthelife = TextField('Describe a day in the life of your rescued Ridgeback',
                             [validators.Required(), validators.Length(min=1, max=1024)])
    dogasfamily = TextField('Will your rescued Ridgeback be a member of the family?',
                            [validators.Required(), validators.Length(min=1, max=1024)])
    activitylevel = TextField('Describe the activity level of your family / household',
                              [validators.Required(), validators.Length(min=1, max=1024)])
    awaycare = TextField('Who will care for your rescued Ridgeback in your absense?',
                         [validators.Required(), validators.Length(min=1, max=1024)])
    giveup = TextField('If you can no longer care for your rescued Ridgeback, what will happen to him/her?',
                       [validators.Required(), validators.Length(min=1, max=1024)])
    # Housing
    choices = ['house', 'townhome', 'apartment', 'condo', 'mobile home', 'ranch', 'farm', 'duplex', 'other']
    housing = SelectField('What type of dwelling do you live in?',
                          validators=[validators.Required()],
                          choices=[(val, val.capitalize()) for val in choices])
    choices = ['own', 'rent']
    ownrent = SelectField('Do you own or rent?',
                          validators=[validators.Required()],
                          choices=[(val, val.capitalize()) for val in choices])
    landlordproof = SelectField('If you rent, proof of your landlord\'s permission to have a dog will be required.  Are you able to provide this?',
                                choices=[('na', 'N/A'), ('yes', 'Y'), ('no', 'N')])
    yard = SelectField('Do you have a yard?',
                       choices=[('yes', 'Y'), ('no', 'N')])
    fence = SelectField('If yes, do you have a fence?',
                        choices=[('yes', 'Y'), ('no', 'N')])
    fencedetails = TextField('If yes, what is the fencing material and its height?')
    # Ridgeback preferences
    ridgebackname = TextField('If there is a specific Ridgeback you are interested in adopting, what is his / her name?',
                              [validators.Optional(), validators.Length(max=256)])
    ridgebackgender = SelectField('Gender',
                                  choices=[('either', 'Either'), ('male', 'M'), ('female', 'F')])
    ridgebackage = TextField('Age', [validators.Optional(), validators.Length(max=256)])
    ridgebackridges = SelectField('With or without a ridge',
                                  choices=[('either', 'Either'), ('ridged', 'Ridged'), ('ridgeless', 'Ridgeless')])
    ridgebackpurebred = SelectField('Purebred vs. Mix',
                                    choices=[('either', 'Either'), ('purebred', 'Purebred'), ('mixed', 'Mixed')])
    ridgebackhealthproblems = TextField('Are you willing to adopt a dog with health problems?',
                                        [validators.Optional(), validators.Length(max=1024)])
    ridgebacksocialproblems = TextField('Are you willing to adopt a dog with social problems?',
                                        [validators.Optional(), validators.Length(max=1024)])

    submit = SubmitField('Apply')
