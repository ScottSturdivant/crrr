# from crrr import uploaded_photos, app
from werkzeug.datastructures import FileStorage
from crrr.dogs import constants as DOG
from flask.ext.uploads import UploadSet, IMAGES
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileAllowed, FileField
from wtforms import (
    IntegerField,
    TextField,
    SelectField,
    BooleanField,
    SubmitField,
    FieldList,
    TextAreaField,
    validators
)

images = UploadSet('images', IMAGES)


class DogMixin(Form):
    name = TextField('Name', [validators.Required('A name is required.')])
    breed = TextField('Breed')
    sex = SelectField('Sex', choices=[(str(key), val.capitalize()) for key, val in DOG.SEX.iteritems()])
    status = SelectField('Status', choices=[(str(key), val.capitalize()) for key, val in DOG.STATUS.iteritems()])
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

    uploads = FieldList(
        FileField('Picture', validators=[FileAllowed(images, 'Images only!')]),
        min_entries=3
    )


class AddDog(DogMixin):
    send = SubmitField('Add Dog')


class EditDog(DogMixin):
    happy_tails = TextAreaField('Happy Tails')
    archive = BooleanField('Archive')
    send = SubmitField('Update Dog')

    def __init__(self, *args, **kwargs):
        DogMixin.__init__(self, *args, **kwargs)
        if "obj" in kwargs:
            dog = kwargs['obj']
            self.id = dog.id
            for i, picture in enumerate(dog.pictures):
                self.uploads.entries[i].data = FileStorage(filename=picture.thumb_url)
