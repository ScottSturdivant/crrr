import sqlite3
from flask import Flask, g
from flask.ext.mail import Mail
from datetime import datetime
from contextlib import closing

def get_year():
    return datetime.now().year

app = Flask(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
app.config['DATABASE'] = '/home/scott/CRRR/crrrescue.db'
app.secret_key = "k\x08\r\xdd'\xb0W\xff\xc9\x0b\x9br\x07\xefW\x9c\x80\x18\xbbP\xb7\xad\xa4\xc9"
app.jinja_env.globals.update(get_year=get_year)
mail = Mail(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


import crrr.views
