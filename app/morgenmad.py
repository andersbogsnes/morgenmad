from flask import Flask

from app.views import main_view
from app.user.views import user_blueprint
from app.api.user import user_api
from app.extensions import db, bcrypt, login_manager, migrate, csrf, mail
from app.model import User



def create_app(config):
    app = Flask('morgenmad')
    app.config.from_object(config)
    app = register_extensions(app)
    app = register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db=db)
    csrf.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'user.login'
    login_manager.refresh_view = 'main.main'

    return app


def register_blueprints(app):
    app.register_blueprint(main_view)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(user_api)
    return app
