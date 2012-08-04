import re
from crrr.states import STATES
from wtforms import (
    Form,
    IntegerField,
    TextField,
    SelectField,
    BooleanField,
    PasswordField,
    validators
    )


class ApplicationForm(Form):
    pass

class Address(Form):
    addr_1     = TextField("Address Line 1", [validators.Length(min=1, max=128)])
    addr_2     = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    city       = TextField("City", [validators.Length(min=1, max=128)])
    state      = SelectField("State", [validators.Required()], choices=sorted(zip(STATES,STATES)))
    zip_code   = TextField("Zip Code", [validators.Regexp('^(\d{5}(-\d{4})?)?$')])

class PersonalInfo(Address):
    first_name = TextField("First Name", [validators.Length(min=1, max=25)])
    last_name  = TextField("Last Name", [validators.Length(min=1, max=35)])
    email      = TextField("Email", [validators.Email()])
    phone      = TextField("Phone", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_h    = TextField("Phone (h)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_c    = TextField("Phone (c)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_w    = TextField("Phone (w)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])


class Volunteer(PersonalInfo):
    foster    = BooleanField(label='Be a foster family for a rescued Ridgeback.')
    transport = BooleanField(label=('Help transport a rescue dog.  For example, '
                                    'to and from a vet appointment or from a '
                                    'surrenduring situation to foster care.'))
    home_check = BooleanField(label='Help with home checks for a prospective adopter.')
    adopter_check = BooleanField(label=('Help with reference checks for a prospective '
                                        'adopter.  This requires telephone time.'))
    donate_crate = BooleanField(label='Donate a large dog crate.')
    donate_supplies = BooleanField(label='Buy food or dog supplies such as beds, leashes, collars, etc.')
    other = BooleanField(label='Other')

class Login(Form):
    username = TextField("Username", [validators.Length(max=12)])
    password = PasswordField("Password", [validators.Required()])
