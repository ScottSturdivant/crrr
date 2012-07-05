import re
from crrr.states import states
from wtforms import (
    Form,
    IntegerField,
    TextField,
    SelectField,
    SelectMultipleField,
    PasswordField,
    validators
    )


class ApplicationForm(Form):
    pass

class PersonalInfo(Form):
    first_name = TextField("First Name", [validators.Length(min=1, max=25)])
    last_name  = TextField("Last Name", [validators.Length(min=1, max=35)])
    addr_1     = TextField("Address Line 1", [validators.Length(min=1, max=128)])
    addr_2     = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    city       = TextField("City", [validators.Length(min=1, max=128)])
    email      = TextField("Email", [validators.Email()])
    zip_code   = TextField("Zip Code", [validators.Regexp('^(\d{5}(-\d{4})?)?$')])
    state      = SelectField("State", [validators.Required()], choices=states)
    phone      = TextField("Phone", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])


class VolunteerForm(PersonalInfo):
    duty = SelectMultipleField("Duty", 
                               choices=[('drive', 'Drive some doggies.'),
                                        ('food',  'Provide some doggie food.'),
                                        ('check', 'Home checks.')]
                              )
