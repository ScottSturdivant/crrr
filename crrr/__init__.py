from flask import Flask
from flask.ext.mail import Mail
app = Flask(__name__)
mail = Mail(app)
import crrr.views
