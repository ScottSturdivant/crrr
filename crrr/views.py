from flask import request, session, render_template, flash, g
from flaskext.mail import Message
from crrr import app, mail
from crrr.forms import Login, Volunteer

@app.route('/')
def index():
    g.index = True
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
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
    return render_template('about.html') 

@app.route('/faq')
def faq():
    g.faq = True
    return render_template('faq.html')

@app.route('/available_dogs')
def available_dogs():
    g.available_dogs = True
    return render_template('layout.html')

@app.route('/application')
def application():
    g.application = True
    return render_template('layout.html')

@app.route('/happy_tails')
def happy_tails():
    g.happy_tails = True
    return render_template('layout.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    g.volunteer = True
    if request.method == 'GET':
        return render_template('volunteer.html', form=Volunteer())
    elif request.method == 'POST':
        volunteer = Volunteer(request.form)
        if volunteer.validate():
            name = volunteer.first_name.data + " " + volunteer.last_name.data
            msg = Message("%s Volunteer Application Submittal" % name,
                          sender=(name, volunteer.email.data),
                          recipients=[app.config.get('CRRR_EMAIL'),
                                      (name, volunteer.email.data)])
            msg.html = render_template('email_volunteer.html', form=volunteer),
            mail.send(msg)
            return render_template('volunteer.html')
        return render_template('volunteer.html', form=volunteer)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
