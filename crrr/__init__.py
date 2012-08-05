from flask import Flask
from flask.ext.mail import Mail
from datetime import datetime

def get_year():
    return datetime.now().year

app = Flask(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
app.jinja_env.globals.update(get_year=get_year)
mail = Mail(app)
import crrr.views
