import os
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# bp = Blueprint('main', __name__, url_prefix='/')

import config

db = SQLAlchemy()
migrate = Migrate()

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route("/")
    def hello():
        return "Hello World!"

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # Blueprints
    from .api import bp_api

    app.register_blueprint(bp_api)
    from .viewer import bp_viewer

    app.register_blueprint(bp_viewer)

    return app
