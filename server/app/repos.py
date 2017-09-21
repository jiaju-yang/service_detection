import sys

from .domain.repos import AdminRepo, HostRepo
from .models import AdminModel
from .mappers import admin_model_2_admin, admin_2_admin_model
from .domain.entities import Admin
from . import db


class AdminRepoImpl(AdminRepo):
    def get(self):
        admin_models = AdminModel.query.all()
        if len(admin_models) == 0:
            print('You should create a administrator!', file=sys.stderr)
            sys.exit(1)
        if len(admin_models) > 1:
            print('Only one administrator is supported!', file=sys.stderr)
            sys.exit(1)
        return admin_model_2_admin(admin_models[0])

    def set(self, admin: Admin):
        admin_model = admin_2_admin_model(admin)
        exist_admin_model = AdminModel.query.get(1)
        if exist_admin_model:
            admin_model.id = exist_admin_model.id
            db.session.merge(admin_model)
        else:
            db.session.add(admin_model)
        db.session.commit()


class HostRepoImpl(HostRepo):
    def all(self):
        pass