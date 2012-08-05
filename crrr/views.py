from flask import request, session, render_template, flash
from flaskext.mail import Message
from crrr import app, mail
from crrr.forms import Login, Volunteer

@app.route('/')
def index():
    return 'Hello World.'

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
    return render_template('about.html') 

@app.route('/faq')
def faq():
    pass

@app.route('/available_dogs')
def available_dogs():
    pass

@app.route('/application')
def application():
    pass

@app.route('/happy_tails')
def happy_tails():
    pass

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
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
