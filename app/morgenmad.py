from flask import Flask

from app.views import main_view
from app.extensions import db, bcrypt, login_manager, migrate
from app.model import User, Morgenmad



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app = register_extensions(app)
    app = register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db=db)
    return app


def register_blueprints(app):
    app.register_blueprint(main_view)
    return app
