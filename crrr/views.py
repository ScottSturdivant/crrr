from flask import request, session, render_template
from crrr import app
from crrr.forms import Login

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
    pass

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

@app.route('/volunteer')
def volunteer():
    pass
