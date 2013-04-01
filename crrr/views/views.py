from flask import request, session, render_template, flash, g, url_for, redirect
from flask.ext.mail import Message
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import Pagination
from crrr import app, mail, login_manager
from crrr.models import User, Dog
from crrr.forms import (
    Login,
    Volunteer,
    Application,
    )

@app.route('/')
def index():
    g.index = True
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    g.title = 'CRRR - Login'
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        login_user(user, remember=form.remember_me.data)
        flash('You have logged in.')
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/admin/')
@login_required
def admin():
    g.title = "CRRR - Admin"
    show_archived_dogs = request.args.get('showarchiveddogs')
    if show_archived_dogs:
        dogs = Dog.query.order_by(Dog.name).all()
    else:
        dogs = Dog.query.filter_by(archive=False).order_by(Dog.name).all()
    return render_template('admin.html', dogs=dogs)

@app.route('/about/')
def about():
    g.about = True
    g.title = "CRRR - About"
    return render_template('about.html')

@app.route('/faq/')
def faq():
    g.faq = True
    g.title = "CRRR - FAQ"
    return render_template('faq.html')

@app.route('/available_dogs/')
def available_dogs():
    g.available_dogs = True
    g.title = "CRRR - Available Dogs"
    dogs = Dog.query.filter_by(status='adoptable').order_by(Dog.name).all()
    return render_template('available.html', dogs=dogs)

@app.route('/application/', methods=['GET', 'POST'])
def application():
    g.application = True
    g.title = "CRRR - Application"
    form = Application(ridgebackname=request.args.get('dog'))
    if form.validate_on_submit():
        pass
    return render_template('application.html', form=form)

PER_PAGE = 10
@app.route('/happy_tails/', defaults={'page': 1})
@app.route('/happy_tails/page/<int:page>')
def happy_tails(page):
    g.happy_tails = True
    g.title = "CRRR - Happy Tails"
    pagination = Dog.query.filter(Dog.happy_tails != None).filter(Dog.status == 'adopted').order_by(Dog.name).paginate(page, PER_PAGE)
    return render_template('happy_tails.html', dogs=pagination.items, pagination=pagination)

@app.route('/volunteer/', methods=['GET', 'POST'])
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
        msg.html = render_template('email_volunteer.html', form=form),
        mail.send(msg)
        return render_template('volunteer.html')
    return render_template('volunteer.html', form=form)

@app.route('/dog/<int:id>', methods=['GET','POST'])
@login_required
def dog(id):
    g.title = 'CRRR - Edit Dog'
    dog = Dog.query.filter_by(id=id).first_or_404()
    return render_template('dog.html', dog=dog)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.before_request
def before_request():
    g.user = current_user