import string
import random
from datetime import (
        timedelta,
        datetime
        )
from flask import render_template, flash, url_for, abort
from flask.ext.login import login_required
from crrr import app, db
from crrr.models import (
        User,
        Confirm,
        Reset,
        )
from crrr.forms import (
        CreateUser,
        ResetPassword,
        Email,
        Login,
        )

def create_hash():
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))

@app.route('/user/register/', methods=['GET', 'POST'])
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
        # TODO: send email with confirmation link
        flash('A confirmation email has ben sent your way.')
        return "User %s created with confirmation hash: %s" % (user, hash)
    else:
        return render_template('user/register.html', form=form)

@app.route('/user/confirm/<hash>')
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
    return render_template('user/confirm.html', user=user)

@app.route('/user/edit/')
@login_required
def edit():
    return 'Edit'

@app.route('/user/reset/<hash>/', methods=['GET', 'POST'])
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
        return render_template('login.html', form=login)
    else:
        return render_template('/user/reset_hash.html', form=form)

@app.route('/user/reset/', methods=['GET', 'POST'])
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
        return render_template('/user/reset.html', form=form)
