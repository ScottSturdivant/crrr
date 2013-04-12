from crrr import uploaded_photos, app
from crrr.dogs import constants as DOG
from flask.ext.uploads import UploadNotAllowed
from flask.ext.wtf import (
    Form,
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
    TextAreaField,
    FileField,
    validators
    )


class AddDog(Form):
    name = TextField('Name', [validators.Required('A name is required.')])
    breed = TextField('Breed')
    sex = SelectField('Sex', choices=[(str(key), val.capitalize()) for key, val in DOG.SEX.iteritems()])
    status = SelectField('Status', choices=[(str(key), val.capitalize()) for key,val in DOG.STATUS.iteritems()])
    age = SelectField('Age', choices=[(str(key), val.capitalize()) for key, val in DOG.AGE.iteritems()])
    mix = SelectField('Mixed Breed?', choices=[('0', 'N'), ('1', 'Y')])
    size = SelectField('Size (when grown)', choices=[(str(key), val.capitalize()) for key, val in DOG.SIZE.iteritems()])
    fee = IntegerField('Fee', [validators.Optional()])
    description = TextAreaField('Description')
    special_needs = BooleanField('Special Needs')
    home_without_dogs = BooleanField('Home without dogs')
    home_without_cats = BooleanField('Home without cats')
    home_without_kids = BooleanField('Home without children')
    fixed = BooleanField('Spayed / Neutered')
    shots = BooleanField('Up to date with shots')
    housetrained = BooleanField('Housetrained')

    uploads = FieldList(FileField('Picture'), min_entries=3)

    send = SubmitField('Send')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.fnames = {}
        self.pictures = []

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        for i, photo in enumerate(self.uploads.entries):
            if photo.has_file():
                try:
                    filename = uploaded_photos.save(photo.file)
                except UploadNotAllowed:
                    self.errors.append("This is not a valid image.")
                    return False
                else:
                    self.fnames[i] = filename
            else:
                self.fnames[i] = None

        return True

class EditDog(AddDog):
    happy_tails = TextAreaField('Happy Tails')
    archive = BooleanField('Archive')

    def __init__(self, *args, **kwargs):
        AddDog.__init__(self, *args, **kwargs)
        if "obj" in kwargs:
            for i, picture in enumerate(kwargs["obj"].pictures):
                self.fnames[i] = picture.file_url
                self.pictures.append(picture)
