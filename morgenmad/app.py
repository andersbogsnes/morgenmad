from flask import Flask, render_template
from morgenmad.public.views import public
from morgenmad.user.views import user_blueprint
from morgenmad.extensions import db, bcrypt, login_manager, migrate, mail, ma
from morgenmad.config import ProdConfig


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db=db)
    mail.init_app(app)
    ma.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public)
    app.register_blueprint(user_blueprint)
    return None

def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template(f'{error_code}.html'), error_code
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
