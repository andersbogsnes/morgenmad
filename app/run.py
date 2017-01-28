from app.morgenmad import create_app
from app.views import main_view
from app.config import DevConfig


def register_extensions(app):
    return app


def register_blueprints(app):
    app.register_blueprint(main_view)
    return app

app = create_app()
app.config.from_object(DevConfig)
app = register_blueprints(app)
app = register_extensions(app)

app.run()

