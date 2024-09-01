from flask import Flask
from flask_migrate import Migrate
from src.config.database import ConfigDB
from src.celery_app import make_celery
from src.init_db import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigDB)

    db.init_app(app)
    migrate.init_app(app, db)

    celery = make_celery(app)
    app.celery = celery

    from src.routes.batch_router import batches_bp

    app.register_blueprint(batches_bp, url_prefix="/batches")

    return app
