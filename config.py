import os

from paths import APP_ROOT_PATH

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_URL = os.environ.get('DB_URL')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS').split(
        ',') if os.environ.get('ALLOWED_ORIGINS') else []
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
    HOST = os.environ.get('HOST')
    PROPAGATE_EXCEPTIONS=False
    MAIL_SERVER=os.environ.get('EMAIL_SMTP_SERVER')
    MAIL_PORT=os.environ.get('EMAIL_SMTP_PORT')
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.environ.get('EMAIL_USERNAME')
    MAIL_ORDERS_USERNAME=os.environ.get('EMAIL_ORDERS_USERNAME')
    MAIL_UNSUBSCRIBE_USERNAME=os.environ.get('EMAIL_UNSUBSCRIBE_USERNAME')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASSWORD')
    CACHE_TYPE='simple'

class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    ENV = "development"
    TESTING = True
