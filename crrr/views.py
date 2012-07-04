from crrr import app

@app.route('/')
def index():
    return 'Hello World.'

@app.route('/admin')
def admin():
    pass

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
