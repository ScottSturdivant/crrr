from flask import Flask
from flask.ext.mail import Mail
app = Flask(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
mail = Mail(app)
import crrr.views
