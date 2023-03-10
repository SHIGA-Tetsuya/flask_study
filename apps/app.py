from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

# instantiation of SQLAlchemy
db = SQLAlchemy()

csrf = CSRFProtect()

# instantiation of LoginManager
login_manager = LoginManager()
# set end point to which redirect if users haven't logged in
login_manager.login_view = "auth.signup"
# set message which will be displayed when users log in
# set empty message
login_manager.login_message = ""


def create_app(config_key):
    app = Flask(__name__)
    # configuration of app
    app.config.from_object(config[config_key])

    # custom error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    db.init_app(app)
    Migrate(app, db)
    # cooperate login_manager with the app
    login_manager.init_app(app)
    from apps.auth import views as auth_views
    from apps.crud import views as crud_views
    from apps.detector import views as dt_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(dt_views.dt)
    return app


# error end point
def page_not_found(e):
    return render_template("404.html"), 404


def internal_server_error(e):
    return render_template("500.html"), 500
