import sqlite3
from flask import Flask, g, request, url_for
from flask.ext.mail import Mail
from datetime import datetime
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

# For jinja footer template
def get_year():
    return datetime.now().year

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

# Defaults
UPLOADED_PHOTOS_DEST = '/tmp/photos'

# Application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['MAIL_FAIL_SILENTLY '] = False
app.config['CRRR_EMAIL'] = 'adoptions@coloradorhodesianridgebackrescue.org'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/crrr_test.db'
app.secret_key = "k\x08\r\xdd'\xb0W\xff\xc9\x0b\x9br\x07\xefW\x9c\x80\x18\xbbP\xb7\xad\xa4\xc9"
app.config.from_envvar('CRRR_SETTINGS')
app.jinja_env.globals.update(get_year=get_year)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
# Create a mail handler
mail = Mail(app)
# And a database
db = SQLAlchemy(app)
# And a login manager
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'user.login'

# Uploads
uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# Models
from crrr.user.models import *
from crrr.dogs.models import *
from crrr.root.models import *

# Blueprints
from crrr.user.views import mod as userModule
from crrr.root.views import mod as rootModule
from crrr.dogs.views import mod as dogsModule
from crrr.admin.views import mod as adminModule
app.register_blueprint(rootModule)
app.register_blueprint(userModule)
app.register_blueprint(dogsModule)
app.register_blueprint(adminModule)
