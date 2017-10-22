import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Yes, I can.'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_VALID_PERIOD_IN_DAY = 7


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-data.db')


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test-data.db')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'prod-data.db')


config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
