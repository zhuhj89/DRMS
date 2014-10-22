__author__ = 'cnnic'
import os
from flask import Flask, abort, url_for, request
from extensions import db, login_manager, photos
import logging
from logging import StreamHandler
from logging.handlers import SMTPHandler, RotatingFileHandler
from app.views import domain, site, user, product, reg, admin
from flask.ext.uploads import configure_uploads
from flask.ext.babel import Babel, gettext as _
logger = logging.getLogger(__name__)

DEFAULT_APP_NAME = 'app'

DEFAULT_MODULES = (
    (site, '/'),
    (user, '/user'),
    (domain, "/domain"),
    (product, "/product"),
    (reg, '/reg'),
    (admin, '/admin'),
)


def create_app(config=None, modules=None):
    logger.info("Setting up Appliaction")
    if modules is None:
        modules = DEFAULT_MODULES
    app = Flask(DEFAULT_APP_NAME)
    app.config.from_pyfile(config)
    configure_extensions(app)
    configure_logging(app)
    configure_uploads(app, (photos,))
    configure_template_filters(app)
    configure_i18n(app)
    configure_modules(app, modules)
    return app


def configure_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

    @app.after_request
    def after_request(response):
        try:
            db.session.commit()

        except Exception,e:
            print e,"++++++++++++++++++++"
            db.session.rollback()
            abort(500)
        return response

def configure_modules(app, blueprints):

    for module, url_prefix in blueprints:
        app.register_blueprint(module, url_prefix=url_prefix)

def configure_template_filters(app):
    from app.utils.filters import dateformat, empty, time_passed, \
                                        error_class, error_text
    app.jinja_env.filters['error_class'] = error_class
    app.jinja_env.filters['error_text'] = error_text
    app.jinja_env.filters['dateformat'] = dateformat
    app.jinja_env.filters['empty'] = empty
    app.jinja_env.filters['time_passed'] = time_passed
    app.jinja_env.globals['static'] = (lambda filename: \
            url_for('static', filename=filename))

def configure_i18n(app):

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES',['en','zh'])
        return request.accept_languages.best_match(accept_languages)


def configure_logging(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    print app.config['DEBUG_LOG']
    debug_log = os.path.join(app.root_path,
                             app.config['DEBUG_LOG'])

    debug_file_handler = \
        RotatingFileHandler(debug_log, mode='w+',
                            maxBytes=100000,
                            backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_log = os.path.join(app.root_path,
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


