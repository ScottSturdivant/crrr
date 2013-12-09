import string
import random
from datetime import (
        timedelta,
        datetime
        )
from flask import request, session, render_template, flash, g, url_for, redirect, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from crrr import app, mail, login_manager, db
from crrr.dogs.models import Dog
from crrr.admin.models import User, Confirm, Reset
from crrr.admin.forms import (
        CreateUser,
        ResetPassword,
        Email,
        Login,
        )


mod = Blueprint('admin', __name__, url_prefix='/admin')

@mod.route('/')
@login_required
def index():
    g.title = "CRRR - Admin"
    show_archived_dogs = request.args.get('showarchiveddogs')
    if show_archived_dogs:
        dogs = Dog.query.order_by(Dog.name).all()
    else:
        dogs = Dog.query.filter_by(archive=False).order_by(Dog.name).all()
    return render_template('admin/index.html', dogs=dogs)

def create_hash():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))

@mod.route('/register/', methods=['GET', 'POST'])
def register():
    form = CreateUser()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        # Now the confirmation hash associated with this user
        hash = create_hash()
        confirm = Confirm(hash=hash)
        user.confirmation = confirm
        db.session.add(user)
        db.session.commit()
        # Send an email with confirmation link
        msg = Message('Your CRRR account has been created!',
                      sender='info@crrr.org',
                      recipients=[user.email])
        msg.body = 'Please visit %s to complete your account registration.' % (url_for('user.confirm', hash=hash, _external=True))
        mail.send(msg)
        flash('A confirmation email has been sent your way.')
        return redirect(url_for("user.login"))
    else:
        return render_template('admin/register.html', form=form)

@mod.route('/confirm/<hash>')
def confirm(hash):
    result = db.session.query(Confirm, User).join(User).\
                      filter(Confirm.hash==hash).\
                      first()
    if result is None:
        abort(404)

    confirm, user = result
    user.active = True
    db.session.delete(confirm)
    db.session.flush()
    db.session.commit()
    return render_template('admin/confirm.html', user=user)

def reset_hash(hash):
    result = db.session.query(User, Reset).join(Reset).\
                        filter(Reset.hash==hash).\
                        first()
    print result
    if result is None:
        abort(404)

    form = ResetPassword()
    if form.validate_on_submit():

        # They exist!
        user, reset = result

        # The user has an hour to reset their password
        allowable_delta = timedelta(hours=1)
        actual_delta = datetime.utcnow() - reset.timestamp
        if actual_delta > allowable_delta:
            db.session.delete(reset)
            db.session.commit()
            return 'Too slow!'

        user, reset = result
        user.set_password(form.password.data)
        db.session.delete(reset)
        db.session.commit()
        flash('Your password was successfully reset.')
        login = Login()
        return render_template('admin/login.html', form=login)
    else:
        return render_template('admin/reset_hash.html', form=form)

@mod.route('/reset/', methods=['GET', 'POST'])
def reset():
    form = Email()
    if form.validate_on_submit():
        # TODO email
        reset = Reset(hash=create_hash(),
                      user_id=form.user.id)
        db.session.add(reset)
        db.session.commit()
        flash('An email has been sent with instructions for resetting your password.')
        return render_template('index.html')
    else:
        return render_template('admin/reset.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    g.title = 'CRRR - Login'
    g.login = True
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        login_user(user, remember=form.remember_me.data)
        flash('You have logged in.')
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template('admin/login.html', form=form)

@mod.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('root.index'))

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
