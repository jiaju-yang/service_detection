from .repos import sqlalchemy, AdminRepoImpl, HostRepoImpl, ServiceRepoImpl
from . import tables


def get_repos(app):
    sqlalchemy.init_app(app)

    return {
        'admin': AdminRepoImpl(),
        'host': HostRepoImpl(),
        'service': ServiceRepoImpl(),
    }


def init(app):
    with app.app_context():
        tables.create_all(sqlalchemy.engine)
