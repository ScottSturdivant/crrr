from flask import request, session, render_template, flash, g, url_for, redirect, Blueprint
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from crrr import app, mail, login_manager
from crrr.user.models import User
from crrr.dogs.models import Dog
from crrr.root.forms import (
    Volunteer,
    Application,
    )

mod = Blueprint('root', __name__, url_prefix='/')

@mod.route('/')
def index():
    g.index = True
    return render_template('root/index.html')

@mod.route('about/')
def about():
    g.about = True
    g.title = "CRRR - About"
    return render_template('root/about.html')

@mod.route('faq/')
def faq():
    g.faq = True
    g.title = "CRRR - FAQ"
    return render_template('root/faq.html')

@mod.route('application/', methods=['GET', 'POST'])
def application():
    g.application = True
    g.title = "CRRR - Application"
    form = Application(ridgebackname=request.args.get('dog'))
    if form.validate_on_submit():
        pass
    return render_template('root/application.html', form=form)

@mod.route('volunteer/', methods=['GET', 'POST'])
def volunteer():
    g.volunteer = True
    g.title = "CRRR - Volunteer"
    form = Volunteer()
    if form.validate_on_submit():
        name = form.first_name.data + " " + form.last_name.data
        msg = Message("%s Volunteer Application Submittal" % name,
                      sender=(name, form.email.data),
                      recipients=[app.config.get('CRRR_EMAIL'),
                                  (name, form.email.data)])
        msg.html = render_template('root/email_volunteer.html', form=form),
        mail.send(msg)
        return render_template('root/volunteer.html')
    return render_template('root/volunteer.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.before_request
def before_request():
    g.user = current_user
