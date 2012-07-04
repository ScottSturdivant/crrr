import re
from wtforms import Form, IntegerField, TextField, PasswordField, validators


class Phone(object):
    def __init__(self,
                 regex='^\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})$',
                 message=None):
        if message is not None:
            message = u'Not a valid telephone (NNN) NNN-NNNN.'
        self.message = message
        self.regex = regex

    def __call__(self, form, field):
        return validators.Regexp(self.regex)


class ApplicationForm(Form):
    pass

class VolunteerForm(Form):
    first_name = TextField("First Name", [validators.Length(min=1, max=25)])
    last_name  = TextField("Last Name", [validators.Length(min=1, max=35)])
    addr_1     = TextField("Address Line 1", [validators.Length(min=1, max=128)])
    addr_2     = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    city       = TextField("City", [validators.Length(min=1, max=128)])
    email      = TextField("Email", [validators.Email()])
    zip_code   = TextField("Zip Code", [validators.Regexp('^\d{5}(-\d{4})?$')])
    phone      = TextField("Phone",
                 [#validators.Optional(),
                  validators.Regexp('^\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})$')])
