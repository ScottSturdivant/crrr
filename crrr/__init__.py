from flask import Flask
from flask.ext.mail import Mail
from datetime import datetime

def get_year():
    return datetime.now().year

app = Flask(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
app.secret_key = "k\x08\r\xdd'\xb0W\xff\xc9\x0b\x9br\x07\xefW\x9c\x80\x18\xbbP\xb7\xad\xa4\xc9"
app.jinja_env.globals.update(get_year=get_year)
mail = Mail(app)
import crrr.views
