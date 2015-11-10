import os
import glob
import random
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

def get_static_abspath():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

def get_random_header_image():
    """Returns a random header image."""
    header_img_dir = os.path.join(get_static_abspath(), 'images/headers')
    header_imgs = glob.glob(os.path.join(header_img_dir, 'header_*'))
    return os.path.basename(random.choice(header_imgs))

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
app.jinja_env.globals['get_random_header_image'] = get_random_header_image

# Logging
if not app.debug:
    # We'll send emails for anything that's important, and shove everything
    # else into a file.
    import logging
    from logging import Formatter
    from logging.handlers import SMTPHandler, RotatingFileHandler
    mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                               app.config['MAIL_DEFAULT_SENDER'],
                               app.config['ADMINS'],
                               'CRRR website error.'
                              )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
    app.logger.addHandler(mail_handler)
    # For for file handling...
    file_handler = RotatingFileHandler(app.config['LOG_FILE_NAME'],
                                       maxBytes=10*1024*1024,
                                       backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
                ))
    app.logger.addHandler(file_handler)

    # Finally, we're really interested in everything the app has to tell us.
    app.logger.setLevel(logging.DEBUG)


# Create a mail handler
mail = Mail(app)
# And a database
db = SQLAlchemy(app)
# And a login manager
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'admin.login'

# Uploads
uploaded_photos = UploadSet('photos', IMAGES)
configure_uploads(app, uploaded_photos)

# Models
from crrr.admin.models import *
from crrr.dogs.models import *
from crrr.root.models import *

# Blueprints
from crrr.root.views import mod as rootModule
from crrr.dogs.views import mod as dogsModule
from crrr.admin.views import mod as adminModule
app.register_blueprint(rootModule)
app.register_blueprint(dogsModule)
app.register_blueprint(adminModule)
