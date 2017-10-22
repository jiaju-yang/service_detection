from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select, update, insert, delete

from .sqlalchemy_helper import choose_columns
from .tables import admins, hosts, services
from .. import db
from ..domain.entities import Admin, Host, Service
from ..domain.errors import NoAdministratorFound
from ..domain.repos import AdminRepo, HostRepo, ServiceRepo


class AdminRepoImpl(AdminRepo):
    def get(self):
        with db.engine.connect() as conn:
            admin_data = conn.execute(
                select(choose_columns(admins, 'username',
                                      ('password', 'encrypted_password'),
                                      'sign', 'tip', 'updated_at'))).first()
            if not admin_data:
                raise NoAdministratorFound()
            return Admin(**admin_data)

    def set(self, admin: Admin):
        with db.engine.connect() as conn:
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


class HostRepoImpl(HostRepo):
    def add(self, host: Host):
        with db.engine.connect() as conn:
            conn.execute(
                insert(hosts).values(name=host.name, detail=host.detail,
                                     address=host.address))

    def delete(self, id):
        with db.engine.connect() as conn:
            conn.execute(delete(hosts).where(hosts.c.id == id))

    def all(self):
        session = db.session
        host_entities = session.query(Host).options(joinedload('services')).all()
        session.commit()
        return host_entities

    def modify(self, host: Host):
        with db.engine.connect() as conn:
            conn.execute(update(hosts).where(
                hosts.c.id == host.id).values(
                name=host.name, detail=host.detail,
                address=host.address))


class ServiceRepoImpl(ServiceRepo):
    def add(self, host_id, service: Service):
        with db.engine.connect() as conn:
            conn.execute(
                insert(services).values(
                    name=service.name, detail=service.detail,
                    port=service.port, host_id=host_id))

    def delete(self, id):
        with db.engine.connect() as conn:
            conn.execute(delete(services).where(services.c.id == id))

    def modify(self, host_id, service: Service):
        with db.engine.connect() as conn:
            conn.execute(update(services).where(
                services.c.id == service.id).values(
                name=service.name, detail=service.detail,
                port=service.port, host_id=host_id))
