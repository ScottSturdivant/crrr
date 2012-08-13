from flask import request, session, render_template, flash, g
from flaskext.mail import Message
from crrr import app, mail, query_db
from crrr.forms import (
    Login,
    Volunteer,
    Application,
    )

@app.route('/')
def index():
    g.index = True
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    g.title = "CRRR - Admin"
    if request.method == 'POST':
        login = Login(request.POST)
        if login.validate():
            # TODO - Authenticate
            session['username'] = login.username
            return redirect(url_for('admin'))
    elif request.method == 'GET':
        if 'username' in session:
            print "Logged in!"
        else:
            return render_template('admin.html', form=Login())

@app.route('/about')
def about():
    g.about = True
    g.title = "CRRR - About"
    return render_template('about.html') 

@app.route('/faq')
def faq():
    g.faq = True
    g.title = "CRRR - FAQ"
    return render_template('faq.html')

@app.route('/available_dogs')
def available_dogs():
    g.available_dogs = True
    g.title = "CRRR - Available Dogs"
    dogs = query_db('select * from Dog_info')
    return render_template('available.html', dogs=dogs)

@app.route('/application', methods=['GET', 'POST'])
def application():
    g.application = True
    g.title = "CRRR - Application"
    form = Application()
    if form.validate_on_submit():
        pass
    return render_template('application.html', form=form)

@app.route('/happy_tails')
def happy_tails():
    g.happy_tails = True
    g.title = "CRRR - Happy Tails"
    return render_template('layout.html')

@app.route('/volunteer', methods=['GET', 'POST'])
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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
