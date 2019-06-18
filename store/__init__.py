from celery import Celery
from flask import Flask
from store.config import config

__version__ = '2.0'
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    celery.conf.update(app.config)
    return app


def register_extensions(app):
    from store.extensions import db
    from store.extensions import jwt_manager
    from store.extensions import mail

    db.init_app(app)
    jwt_manager.init_app(app)
    mail.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()


def register_blueprints(app):
    from store.api.routes import api_bp
    from store.celery_mail.routes import email_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(email_bp)
