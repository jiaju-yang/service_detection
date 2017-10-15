from datetime import datetime

from app.domain.entities import Admin, Host, Service
from app.domain.errors import NoAdministratorFound
from app.models import ServiceModel
from tests.unit.utils import FlaskAppEnvironmentMixin
from app import db
from app.repos import AdminRepoImpl, HostRepoImpl, ServiceRepoImpl


class DbEnvironmentMixin(FlaskAppEnvironmentMixin):
    def setUp(self):
        super().setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super().tearDown()


class AdminRepoImplTestCase(DbEnvironmentMixin):
    def test_admin_persistence(self):
        repo = AdminRepoImpl()
        username = 'test'
        password = '123'
        repo.set(Admin(username, datetime.now(), original_password=password))
        admin = repo.get()
        self.assertEqual(admin.username, username)
        self.assertNotEqual(admin.password, password)

    def test_no_admin_create(self):
        repo = AdminRepoImpl()
        self.assertRaises(NoAdministratorFound, repo.get)


class HostRepoImplTestCase(DbEnvironmentMixin):
    def setUp(self):
        super().setUp()
        self.repo = HostRepoImpl()
        self.host1_data = {'name': 'localhost', 'detail': 'this machine',
                           'address': '127.0.0.1'}
        self.host2_data = {'name': 'server1', 'detail': 'remote machine 1',
                           'address': '8.8.8.8'}

    def test_one_host_persistence(self):
        host = Host(**self.host1_data)
        self.repo.add(host)
        hosts_from_persistence = self.repo.all()
        self.assertEqual(len(hosts_from_persistence), 1)
        host_from_persistence = hosts_from_persistence[0]
        for key in self.host1_data.keys():
            self.assertEqual(getattr(host, key),
                             getattr(host_from_persistence, key))

    def test_multiple_host_persistence(self):
        hosts = [Host(**self.host1_data), Host(**self.host2_data)]
        for host in hosts:
            self.repo.add(host)
        hosts_from_persistence = self.repo.all()
        self.assertEqual(len(hosts), 2)
        for host, host_from_persistence in zip(hosts, hosts_from_persistence):
            for key in self.host1_data.keys():
                self.assertEqual(getattr(host, key),
                                 getattr(host_from_persistence, key))

    def test_modify(self):
        host1 = Host(**self.host1_data)
        host2 = Host(**self.host2_data)
        host2.id = 1
        self.repo.add(host1)
        self.repo.modify(host2)
        hosts_from_persistence = self.repo.all()
        self.assertEqual(len(hosts_from_persistence), 1)
        host_from_persistence = hosts_from_persistence[0]
        for key in (list(self.host1_data.keys()) + ['id']):
            self.assertEqual(getattr(host2, key),
                             getattr(host_from_persistence, key))

    def test_delete(self):
        host = Host(**self.host1_data)
        self.repo.add(host)
        self.repo.delete(self.repo.all()[0].id)
        self.assertEqual(len(self.repo.all()), 0)


class ServiceRepoImplTestCase(DbEnvironmentMixin):
    def setUp(self):
        super().setUp()
        self.host_repo = HostRepoImpl()
        self.service_repo = ServiceRepoImpl()
        host_data = {'name': 'localhost', 'detail': 'this machine',
                          'address': '127.0.0.1'}
        host = Host(**host_data)
        self.host_repo.add(host)
        self.service1_data = {'name': 'nginx', 'detail': 'nginx service',
                              'port': 80}
        self.service2_data = {'name': 'postgres', 'detail': 'postgres database',
                              'port': 5432}

    def test_one_service_persistence(self):
        host_from_persistence = self.host_repo.all()[0]
        service = Service(**self.service1_data)
        self.service_repo.add(host_from_persistence.id, service)
        host_from_persistence = self.host_repo.all()[0]
        services_from_persistence = host_from_persistence.services
        self.assertEqual(len(services_from_persistence), 1)
        service_from_persistence = services_from_persistence[0]
        for key in self.service1_data.keys():
            self.assertEqual(getattr(service, key),
                             getattr(service_from_persistence, key))

    def test_modify(self):
        host_from_persistence = self.host_repo.all()[0]
        service = Service(**self.service1_data)
        self.service_repo.add(host_from_persistence.id, service)
        service_from_persistence = self.host_repo.all()[0].services[0]

        modified_service = Service(**self.service2_data)
        modified_service.id = service_from_persistence.id
        self.service_repo.modify(host_from_persistence.id, modified_service)

        services_from_persistence = self.host_repo.all()[0].services
        self.assertEqual(len(services_from_persistence), 1)
        modified_service_from_persistence = services_from_persistence[0]
        for key in (list(self.service1_data.keys()) + ['id']):
            self.assertEqual(getattr(modified_service, key), getattr(modified_service_from_persistence, key))

    def test_delete(self):
        service = Service(**self.service1_data)
        self.service_repo.add(self.host_repo.all()[0].id, service)
        service_id = self.host_repo.all()[0].services[0].id
        self.service_repo.delete(service_id)
        self.assertEqual(len(self.host_repo.all()[0].services), 0)
