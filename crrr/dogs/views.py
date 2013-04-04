from flask import request, session, render_template, flash, g, url_for, redirect, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import Pagination
from crrr import app, mail, login_manager
from crrr.user.models import User
from crrr.dogs.models import Dog
from crrr.root.forms import (
    Volunteer,
    Application,
    )

mod = Blueprint('dogs', __name__, url_prefix='/dogs')

@mod.route('/available/')
def available():
    g.available_dogs = True
    g.title = "CRRR - Available Dogs"
    dogs = Dog.query.filter_by(status='adoptable').order_by(Dog.name).all()
    return render_template('dogs/available.html', dogs=dogs)

PER_PAGE = 20
@mod.route('/happy_tails/', defaults={'page': 1})
@mod.route('/happy_tails/page/<int:page>')
def happy_tails(page):
    g.happy_tails = True
    g.title = "CRRR - Happy Tails"
    pagination = Dog.query.filter(Dog.happy_tails != None).filter(Dog.status == 'adopted').order_by(Dog.name).paginate(page, PER_PAGE)
    return render_template('dogs/happy_tails.html', dogs=pagination.items, pagination=pagination)

@mod.route('/dog/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    g.title = 'CRRR - Edit Dog'
    dog = Dog.query.filter_by(id=id).first_or_404()
    return render_template('dogs/dog.html', dog=dog)
