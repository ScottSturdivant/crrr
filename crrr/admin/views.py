from flask import request, session, render_template, flash, g, url_for, redirect, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from crrr import app, mail, login_manager
from crrr.user.models import User
from crrr.dogs.models import Dog

mod = Blueprint('admin', __name__, url_prefix='/admin/')

@mod.route('/')
#@login_required
def index():
    g.title = "CRRR - Admin"
    show_archived_dogs = request.args.get('showarchiveddogs')
    if show_archived_dogs:
        dogs = Dog.query.order_by(Dog.name).all()
    else:
        dogs = Dog.query.filter_by(archive=False).order_by(Dog.name).all()
    return render_template('admin/index.html', dogs=dogs)
