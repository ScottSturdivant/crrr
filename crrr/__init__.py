import sqlite3
from flask import Flask, g
from flask.ext.mail import Mail
from datetime import datetime
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

def get_year():
    return datetime.now().year

app = Flask(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/scott/CRRR/crrrescue.db'
app.secret_key = "k\x08\r\xdd'\xb0W\xff\xc9\x0b\x9br\x07\xefW\x9c\x80\x18\xbbP\xb7\xad\xa4\xc9"
app.jinja_env.globals.update(get_year=get_year)
# Create a mail handler
mail = Mail(app)
# And a database
db = SQLAlchemy(app)
# And a login manager
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = '/login'
import crrr.views
import crrr.models
