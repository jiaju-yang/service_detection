import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Yes, I can.'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_VALID_PERIOD_IN_DAY = 7


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_data.db')


config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'default': DevConfig
}
