from .repos import sqlalchemy, SqlalchemyAdminRepo, SqlalchemyHostRepo, SqlalchemyServiceRepo
from . import tables


def get_repos(app):
    sqlalchemy.init_app(app)

    return {
        'admin': SqlalchemyAdminRepo(),
        'host': SqlalchemyHostRepo(),
        'service': SqlalchemyServiceRepo(),
    }


def init(app):
    with app.app_context():
        tables.create_all(sqlalchemy.engine)
