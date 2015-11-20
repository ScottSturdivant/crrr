import os
from PIL import Image
from flask import render_template, flash, g, url_for, redirect, Blueprint, request
from flask.ext.login import login_required
from crrr import app, db, uploaded_photos
from crrr.dogs.models import Dog, Picture
from crrr.dogs import constants as DOG
from crrr.dogs.forms import AddDog, EditDog

mod = Blueprint('dogs', __name__, url_prefix='/dogs')

# Thumbnails
THUMB_SIZE = (750, 750)
THUMB_PREFIX = "tb_"

# PAGINATION
PER_PAGE = 20


@mod.route('/')
def index():
    g.title = 'CRRR - Dogs'
    dogs = Dog.query.all()
    return render_template('dogs/index.html', dogs=dogs)


@mod.route('/available/')
def available():
    g.available_dogs = True
    g.title = "CRRR - Available Dogs"
    dogs = Dog.query.filter(Dog.status == DOG.ADOPTABLE).order_by(Dog.name).all()
    return render_template('dogs/available.html', dogs=dogs)


@mod.route('/happy_tails/', defaults={'page': 1})
@mod.route('/happy_tails/page/<int:page>')
def happy_tails(page):
    g.happy_tails = True
    g.title = "CRRR - Happy Tails"
    pagination = Dog.query.filter(Dog.happy_tails != None).filter(Dog.status == DOG.ADOPTED).order_by(Dog.name).paginate(page, PER_PAGE)  # noqa
    return render_template('dogs/happy_tails.html', dogs=pagination.items, pagination=pagination, page=page)


@mod.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    g.title = 'CRRR - Edit Dog'
    dog = Dog.query.filter_by(id=id).first_or_404()
    form = EditDog() if request.method == 'POST' else EditDog(obj=dog)
    if form.validate_on_submit():
        form.populate_obj(dog)
        for i, picture in enumerate(form.uploads):

            # Nothing was actually uploaded for this image
            if not picture.data:
                continue

            app.logger.debug('processing picture: %s', picture)
            # If the picture already exists, delete it
            try:
                p = dog.pictures[i]
            except IndexError:
                p = Picture()

            # Save the file original file
            filename = uploaded_photos.save(picture.data, folder=str(dog.id))

            # Create a thumbnail of this new picture
            thumb = thumbify(uploaded_photos.path(filename))
            p.file_url = os.path.basename(filename)
            p.thumb_url = os.path.basename(thumb)

        db.session.add(dog)
        db.session.commit()
        flash("%s was successfully edited." % dog.name)
        return redirect(url_for('admin.index'))

    return render_template('dogs/edit.html', form=form)


@mod.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    form = AddDog()

    if form.validate_on_submit():
        dog = Dog()
        db.session.add(dog)
        db.session.flush()  # So we can get the ID value
        form.populate_obj(dog)

        pictures = [p for p in form.uploads.entries if p]
        # Create the output directory if required
        for picture in pictures:
            app.logger.debug('adding picture: %s', picture)
            # Save the file original file
            filename = uploaded_photos.save(picture.data, folder=str(dog.id))

            # Create the thumbnail
            thumb = thumbify(uploaded_photos.path(filename))
            p = Picture(file_url=os.path.basename(filename),
                        thumb_url=os.path.basename(thumb))
            dog.pictures.append(p)

        db.session.commit()
        flash("%s was successfully added." % dog.name)
        return redirect(url_for('admin.index'))

    return render_template('dogs/add.html', form=form)


def thumbify(infile):
    out_filename = os.path.join(os.path.dirname(infile), THUMB_PREFIX + os.path.basename(infile))
    img = Image.open(infile)
    img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    img.save(out_filename)
    return out_filename
