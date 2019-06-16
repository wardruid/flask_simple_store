import os

db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db_uri = 'sqlite:///{}'.format(db_path)


class Config(object):
    # DB configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default=db_uri)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', default='dev')
    SECRET_KEY = os.environ.get('SECRET_KEY', default='dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask_jwt_extended configuration
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Celery configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


config = Config
