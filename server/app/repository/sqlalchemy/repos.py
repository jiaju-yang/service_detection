from itertools import groupby
from sqlalchemy import join
from sqlalchemy.sql import select, update, insert, delete
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

from app.domain.entities import Admin, Host, Service
from app.domain.errors import NoAdministratorFound
from app.domain.repos import AdminRepo, HostRepo, ServiceRepo

from .sqlalchemy_helper import choose_columns
from .tables import admins, hosts, services

sqlalchemy = SQLAlchemy()


class SqlalchemyAdminRepo(AdminRepo):
    def get(self):
        with sqlalchemy.engine.connect() as conn:
            admin_data = conn.execute(
                select(choose_columns(admins, 'username',
                                      ('password', 'encrypted_password'),
                                      'sign', 'tip', 'updated_at'))).first()
            if not admin_data:
                raise NoAdministratorFound()
            return Admin(**admin_data)

    def set(self, admin: Admin):
        with sqlalchemy.engine.connect() as conn:
            exist_admin = conn.execute(select([admins.c.id])).first()
            if exist_admin:
                conn.execute(
                    update(admins).where(
                        admins.c.id == exist_admin['id']).values(
                        username=admin.username,
                        updated_at=admin.updated_at,
                        password=admin.password,
                        sign=admin.sign,
                        tip=admin.tip))
            else:
                conn.execute(insert(admins).values(username=admin.username,
                                                   updated_at=admin.updated_at,
                                                   password=admin.password,
                                                   sign=admin.sign,
                                                   tip=admin.tip))


class SqlalchemyHostRepo(HostRepo):
    def next_identity(self):
        return 'HOST_' + str(uuid4())

    def save(self, host: Host):
        with sqlalchemy.engine.connect() as conn:
            exist_host = conn.execute(
                select([hosts.c.id]).where(hosts.c.id == host.id)).first()
            if exist_host:
                conn.execute(
                    update(hosts).where(
                        hosts.c.id == host.id).values(id=host.id,
                                                      name=host.name,
                                                      detail=host.detail,
                                                      address=host.address))
            else:
                conn.execute(
                    insert(hosts).values(id=host.id, name=host.name,
                                         detail=host.detail,
                                         address=host.address))

    def delete(self, id):
        with sqlalchemy.engine.connect() as conn:
            conn.execute(delete(hosts).where(hosts.c.id == id))

    def all(self):
        with sqlalchemy.engine.connect() as conn:
            result = conn.execute(select(choose_columns(hosts, ('id', 'id'),
                                                        ('name', 'name'),
                                                        ('address', 'address'),
                                                        ('detail',
                                                         'detail')) + choose_columns(
                services, ('id', 'service.id'), ('name', 'service.name'),
                ('detail', 'service.detail'), ('port', 'service.port'),
                ('host_id', 'host_id'))).select_from(
                join(hosts, services, hosts.c.id == services.c.host_id,
                     isouter=True)))
            host_models = []
            for host_data, services_data in groupby(
                    result, key=lambda row: {key: row[key] for key in (
                            'id', 'name', 'address', 'detail')}):
                service_models = [Service(service_data['service.name'],
                                          service_data['service.detail'],
                                          service_data['service.port'],
                                          service_data['service.id']) for
                                  service_data in
                                  services_data if service_data['service.id']]
                host_models.append(Host(**host_data, services=service_models))
            return host_models


class SqlalchemyServiceRepo(ServiceRepo):
    def add(self, host_id, service: Service):
        with sqlalchemy.engine.connect() as conn:
            conn.execute(
                insert(services).values(
                    name=service.name, detail=service.detail,
                    port=service.port, host_id=host_id))

    def delete(self, id):
        with sqlalchemy.engine.connect() as conn:
            conn.execute(delete(services).where(services.c.id == id))

    def modify(self, host_id, service: Service):
        with sqlalchemy.engine.connect() as conn:
            conn.execute(update(services).where(
                services.c.id == service.id).values(
                name=service.name, detail=service.detail,
                port=service.port, host_id=host_id))
