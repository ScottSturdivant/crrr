import re
from crrr.states import STATES
from crrr.admin.models import User
from flask.ext.wtf import Form
from wtforms import (
    IntegerField,
    TextField,
    SelectField,
    BooleanField,
    PasswordField,
    SubmitField,
    SelectMultipleField,
    FormField,
    FieldList,
    HiddenField,
    validators
    )
from flask.ext.wtf.html5 import (
    EmailField,
    )


class Email(Form):
    email = EmailField('Email', [validators.Email("This doesn't appear to be a valid email address."),
                                validators.Required('An email address is required.')])
    send = SubmitField('Send')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.email==self.email.data).first()
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
    email = EmailField('Email', [validators.Email("This doesn't appear to be a valid email address."),
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

        user = User.query.filter(User.username==self.username.data).first()
        if user:
            self.username.errors.append('This username is already taken.')
            return False

        user = User.query.filter(User.email==self.email.data).first()
        if user:
            self.email.errors.append('This email address is already in use.')
            return False

        self.user = user
        return True

class Address(Form):
    addr_1     = TextField("Address Line 1", [validators.Length(min=1, max=128), validators.Required()])
    addr_2     = TextField("Address Line 2", [validators.Optional(), validators.Length(max=128)])
    city       = TextField("City", [validators.Length(min=1, max=128), validators.Required()])
    state      = SelectField("State", [validators.Required()], choices=sorted(zip(STATES,STATES)))
    zip_code   = TextField("Zip Code", [validators.Required(), validators.Regexp('^(\d{5}(-\d{4})?)?$')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(Address, self).__init__(*args, **kwargs)

class PersonalInfo(Address):
    first_name = TextField("First Name", [validators.Length(min=1, max=25), validators.Required()])
    last_name  = TextField("Last Name", [validators.Length(min=1, max=35), validators.Required()])
    email      = EmailField("Email", [validators.Email(), validators.Required()])
    phone_h    = TextField("Phone (h)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_c    = TextField("Phone (c)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])
    phone_w    = TextField("Phone (w)", 
                 [validators.Regexp('^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4}))?$')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(PersonalInfo, self).__init__(*args, **kwargs)

    def __iter__(self):
        """Re-order the way the fields are rendered."""
        vals = ['first_name', 'last_name', 'addr_1', 'addr_2', 'city', 'state', 'zip_code',
                'email', 'phone_h', 'phone_c', 'phone_w', 'csrf_token' ]
        for val in vals:
            yield getattr(self, val)


class Login(Form):
    username = TextField("Username", [validators.Required()])
    password = PasswordField("Password", [validators.Required()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.login_errors = []

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter(User.username==self.username.data).first()
        if user is None:
            self.login_errors.append('Incorrect username or password.')
            return False

        if not user.check_password(self.password.data):
            self.login_errors.append('Incorrect username or password.')
            return False

        if not user.active:
            self.login_errors.append('This account is inactive.')
            return False

        return True


