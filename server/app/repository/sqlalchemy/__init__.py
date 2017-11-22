from flask_migrate import Migrate

from .models import db
from .repos import (SqlalchemyAdminRepo, SqlalchemyHostRepo,
                    SqlalchemyServiceRepo)


def get_repos(app):
    db.init_app(app)
    Migrate(app, db)

    return {
        'admin': SqlalchemyAdminRepo(),
        'host': SqlalchemyHostRepo(),
        'service': SqlalchemyServiceRepo(),
    }
