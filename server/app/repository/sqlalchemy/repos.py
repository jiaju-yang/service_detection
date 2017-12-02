from uuid import uuid4

from app.domain.entities import Admin, Host, Service
from app.domain.errors import NoAdministratorFound
from app.domain.repos import AdminRepo, HostRepo, ServiceRepo
from .mappers import (admin_2_admin_model, admin_model_2_admin,
                      host_model_2_host, host_2_host_model,
                      service_2_service_model)
from .models import db, AdminModel, HostModel, ServiceModel


class SqlalchemyAdminRepo(AdminRepo):
    def get(self):
        admin = AdminModel.query.get(1)
        if not admin:
            raise NoAdministratorFound()
        return admin_model_2_admin(admin)

    def set(self, admin: Admin):
        admin_model = admin_2_admin_model(admin)
        admin_model.id = 1
        db.session.merge(admin_model)
        db.session.commit()


class SqlalchemyHostRepo(HostRepo):
    def next_identity(self):
        return 'HOST_' + str(uuid4())

    def save(self, host: Host):
        host_model = host_2_host_model(host)
        db.session.merge(host_model)
        db.session.commit()

    def delete(self, id):
        HostModel.query.filter_by(id=id).delete()
        ServiceModel.query.filter_by(host_id=id).delete()
        db.session.commit()

    def all(self):
        host_models = HostModel.query.all()
        return [host_model_2_host(host_model) for host_model in host_models]

    def host_of_id(self, host_id):
        host_model = HostModel.query.filter_by(id=host_id).first()
        return host_model_2_host(host_model)


class SqlalchemyServiceRepo(ServiceRepo):
    def next_identity(self):
        return 'SERVICE_' + str(uuid4())

    def save(self, host_id, service: Service):
        service_model = service_2_service_model(service, host_id)
        db.session.merge(service_model)
        db.session.commit()

    def delete(self, id):
        ServiceModel.query.filter_by(id=id).delete()
        db.session.commit()
