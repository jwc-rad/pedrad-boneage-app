import os
from pathlib import Path
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# bp = Blueprint('main', __name__, url_prefix='/')

import config

db = SQLAlchemy()
migrate = Migrate()

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = str(Path(os.path.join(PROJECT_DIR, "static")).as_posix())
TEMPLATE_DIR = str(Path(os.path.join(PROJECT_DIR, "templates")).as_posix())
UPLOAD_DIR = str(Path(os.path.join(PROJECT_DIR, "uploads")).as_posix())
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
