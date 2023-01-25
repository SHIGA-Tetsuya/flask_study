from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

# instantiation of SQLAlchemy
db = SQLAlchemy()

csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)
    # configuration of app
    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app, db)
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app
