import sys

from .domain.repos import AdminRepo, HostRepo
from .models import AdminModel, HostModel
from .mappers import admin_model_2_admin, admin_2_admin_model, \
    host_model_2_host, host_2_host_model
from .domain.entities import Admin, Host
from . import db


class AdminRepoImpl(AdminRepo):
    def get(self):
        admins = AdminModel.query.all()
        if len(admins) == 0:
            print('You should create a administrator!', file=sys.stderr)
            sys.exit(1)
        if len(admins) > 1:
            print('Only one administrator is supported!', file=sys.stderr)
            sys.exit(1)
        return admin_model_2_admin(admins[0])

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
    def add(self, host: Host):
        host_model = host_2_host_model(host)
        db.session.add(host_model)
        db.session.commit()

    def all(self):
        hosts = HostModel.query.all()
        return [host_model_2_host(host) for host in hosts]

