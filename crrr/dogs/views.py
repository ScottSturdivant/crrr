import os
from PIL import Image
from flask import request, session, render_template, flash, g, url_for, redirect, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import Pagination
from crrr import app, mail, login_manager, db
from crrr.admin.models import User
from crrr.dogs.models import Dog, Picture
from crrr.dogs import constants as DOG
from crrr.dogs.forms import AddDog, EditDog

mod = Blueprint('dogs', __name__, url_prefix='/dogs')

# Thumbnails
THUMB_SIZE = (100, 100)
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
    dogs = Dog.query.filter(Dog.status==DOG.ADOPTABLE).order_by(Dog.name).all()
    return render_template('dogs/available.html', dogs=dogs)

@mod.route('/happy_tails/', defaults={'page': 1})
@mod.route('/happy_tails/page/<int:page>')
def happy_tails(page):
    g.happy_tails = True
    g.title = "CRRR - Happy Tails"
    pagination = Dog.query.filter(Dog.happy_tails != None).filter(Dog.status==DOG.ADOPTED).order_by(Dog.name).paginate(page, PER_PAGE)
    return render_template('dogs/happy_tails.html', dogs=pagination.items, pagination=pagination, page=page)

@mod.route('/<int:id>/edit', methods=['GET','POST'])
def edit(id):
    g.title = 'CRRR - Edit Dog'
    dog = Dog.query.filter_by(id=id).first_or_404()
    form = EditDog(obj=dog)
    if form.validate_on_submit():
        form.populate_obj(dog)
        for i, picture in form.fnames.iteritems():
            if picture is None:
                continue
            app.logger.debug('processing picture: %s', picture)
            # If the picture already exists, delete it
            try:
                p = dog.pictures[i]
            except IndexError:
                pass
            else:
                app.logger.debug('removing picture: %s', p)
                db.session.delete(p)
                db.session.commit()
            # Create a thumbnail of this new picture
            thumb = thumbify(picture)
            p = Picture(file_url=picture, thumb_url=thumb)
            dog.pictures.insert(i, p)
        db.session.add(dog)
        db.session.commit()
        flash("%s was successfully edited." % dog.name)
        return redirect(url_for('admin.index'))

    return render_template('dogs/edit.html', form=form)

@mod.route('/add/', methods=['GET','POST'])
def add():
    form = AddDog()

    if form.validate_on_submit():
        dog = Dog()
        form.populate_obj(dog)

        pictures = [p for p in form.fnames.values() if p]
        for picture in pictures:
            app.logger.debug('adding picture: %s', picture)
            # Create the thumbnail
            thumb = thumbify(picture)
            p = Picture(file_url=picture, thumb_url=thumb)
            dog.pictures.append(p)

        db.session.add(dog)
        db.session.commit()
        flash("%s was successfully added." % dog.name)
        return redirect(url_for('admin.index'))

    return render_template('dogs/add.html', form=form)


def thumbify(infile):
    app.logger.debug('uploaded dest: %s', app.config['UPLOADED_PHOTOS_DEST'])
    app.logger.debug('infile: %s', infile)
    img = Image.open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], infile))
    img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
    img.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], THUMB_PREFIX + infile))
    return THUMB_PREFIX + infile

       
