# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, g, Blueprint
from flask.ext.mail import Message
from flask.ext.login import current_user
from crrr import app, mail
from crrr.root.forms import (
    Volunteer,
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


@mod.route('breed/')
def breed():
    g.breed = True
    g.title = "CRRR - Breed"
    return render_template('root/breed.html')


@mod.route('faq/')
def faq():
    g.faq = True
    g.title = "CRRR - FAQ"
    return render_template('root/faq.html')


@mod.route('volunteer/', methods=['GET', 'POST'])
def volunteer():
    g.volunteer = True
    g.title = "CRRR - Volunteer"
    form = Volunteer()
    if form.validate_on_submit():
        submitted_at = datetime.now().strftime("%B %d, %Y, %I:%M %p")
        app.logger.info('Volunteer application submitted.')
        app.logger.debug(form.data)
        subject = '{} {} Volunteer Application Submittal'.format(
            form.first_name.data, form.last_name.data
        )
        sender = app.config.get('CRRR_EMAIL')
        msg = Message(subject,
                      sender=sender,
                      recipients=[sender, form.email.data],
                      html=render_template('root/email_volunteer.html',
                                           form=form,
                                           submitted_at=submitted_at)
                      )
        mail.send(msg)
        return render_template('root/volunteer.html')
    return render_template('root/volunteer.html', form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 404


@app.before_request
def before_request():
    g.user = current_user
