import string
import random
from flask import render_template, flash, url_for
from flask.ext.login import login_required
from crrr import app, db
from crrr.models import User
from crrr.forms import CreateUser


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    form = CreateUser()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        # Now the confirmation hash associated with this user
        hash = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(32))
        confirm = Confirm(hash=hash)
        user.confirmation = confirm
        db.session.add(user)
        db.session.commit()
        # TODO: send email with confirmation link
        flash('A confirmation email has ben sent your way.')
        return "User %s created with confirmation hash: %s" % (user, hash)
    else:
        return render_template('register.html', form=form)

@app.route('/user/confirm/<confirmation_hash>')
def confirm(confirmation_hash):
    confirm, user= db.session.query(Confirm, User).join(User).\
                              filter(Confirm.hash=='foobar').first_or_404()
    user.active = True
    db.session.delete(confirm)
    db.session.commit()
    return 'Confirmed!'

@app.route('/user/edit')
@login_required
def edit():
    return 'Edit'
