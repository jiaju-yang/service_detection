from datetime import datetime
import pytest

from app.repository.sqlalchemy.repos import sqlalchemy
from app.domain.entities import Admin, Host, Service
from app.domain.errors import NoAdministratorFound
from app.repository.sqlalchemy import (AdminRepoImpl, HostRepoImpl,
                                       ServiceRepoImpl)
from app.repository.sqlalchemy import tables
from tests.unit.utils import FlaskAppContextEnvironment


class DbEnvironment(FlaskAppContextEnvironment):
    @pytest.fixture
    def table(self, app_context):
        tables.drop_all(sqlalchemy.engine)
        yield tables.create_all(sqlalchemy.engine)
        tables.drop_all(sqlalchemy.engine)


class TestAdminRepoImpl(DbEnvironment):
    @pytest.fixture(scope='class')
    def repo(self):
        return AdminRepoImpl()

    @pytest.fixture
    def admin1_data(self):
        return {
            'username': 'test',
            'original_password': '123',
            'updated_at': datetime.now()
        }

    @pytest.fixture
    def admin2_data(self):
        return {
            'username': 'test2',
            'original_password': '1234',
            'updated_at': datetime.now()
        }

    def test_admin_persistence(self, table, repo, admin1_data):
        repo.set(Admin(**admin1_data))
        admin = repo.get()
        assert admin.username == admin1_data['username']
        assert admin.password != admin1_data['original_password']

    def test_multiple_admin_persistence(self, table, repo, admin1_data,
                                        admin2_data):
        repo.set(Admin(**admin1_data))
        repo.set(Admin(**admin2_data))
        admin = repo.get()
        assert admin.username == admin2_data['username']
        assert admin.password != admin2_data['original_password']

    def test_no_admin_create(self, table, repo):
        with pytest.raises(NoAdministratorFound):
            repo.get()


class TestHostRepoImpl(DbEnvironment):
    @pytest.fixture(scope='class')
    def repo(self):
        return HostRepoImpl()

    @pytest.fixture
    def host1_data(self):
        return {'name': 'localhost', 'detail': 'this machine',
                'address': '127.0.0.1'}

    @pytest.fixture
    def host2_data(self):
        return {'name': 'server1', 'detail': 'remote machine 1',
                'address': '8.8.8.8'}

    def test_one_host_persistence(self, table, repo, host1_data, host2_data):
        host = Host(**host1_data)
        repo.add(host)
        hosts_from_persistence = repo.all()
        assert len(hosts_from_persistence) == 1

        host_from_persistence = hosts_from_persistence[0]
        for key in host1_data.keys():
            assert getattr(host, key) == getattr(host_from_persistence, key)

    def test_multiple_host_persistence(self, table, repo, host1_data,
                                       host2_data):
        hosts = [Host(**host1_data), Host(**host2_data)]
        for host in hosts:
            repo.add(host)
        hosts_from_persistence = repo.all()
        assert len(hosts) == 2

        for host, host_from_persistence in zip(hosts, hosts_from_persistence):
            for key in host1_data.keys():
                assert getattr(host, key) == getattr(host_from_persistence, key)

    def test_modify(self, table, repo, host1_data, host2_data):
        host1 = Host(**host1_data)
        host2 = Host(**host2_data)
        host2.id = 1
        repo.add(host1)
        repo.modify(host2)
        hosts_from_persistence = repo.all()
        assert len(hosts_from_persistence) == 1
        host_from_persistence = hosts_from_persistence[0]
        for key in (list(host1_data.keys()) + ['id']):
            assert getattr(host2, key) == getattr(host_from_persistence, key)

    def test_delete(self, table, repo, host1_data):
        host = Host(**host1_data)
        repo.add(host)
        repo.delete(repo.all()[0].id)
        assert len(repo.all()) == 0


class TestServiceRepoImpl(DbEnvironment):
    @pytest.fixture(scope='class')
    def host_repo(self):
        return HostRepoImpl()

    @pytest.fixture(scope='class')
    def service_repo(self):
        return ServiceRepoImpl()

    @pytest.fixture
    def host_data(self):
        return {'name': 'localhost', 'detail': 'this machine',
                'address': '127.0.0.1'}

    @pytest.fixture
    def service1_data(self):
        return {'name': 'nginx', 'detail': 'nginx service', 'port': 80}

    @pytest.fixture
    def service2_data(self):
        return {'name': 'postgres', 'detail': 'postgres database', 'port': 5432}

    def test_service_persistence(self, table, host_repo, service_repo,
                                 host_data, service1_data, service2_data):
        host_repo.add(Host(**host_data))
        host_from_persistence = host_repo.all()[0]
        service1 = Service(**service1_data)
        service2 = Service(**service2_data)
        service_repo.add(host_from_persistence.id, service1)
        service_repo.add(host_from_persistence.id, service2)

        host_from_persistence = host_repo.all()[0]
        services_from_persistence = host_from_persistence.services
        assert len(services_from_persistence) == 2

        service1_from_persistence = services_from_persistence[0]
        for key in service1_data.keys():
            assert getattr(service1, key) == getattr(service1_from_persistence,
                                                     key)

        service2_from_persistence = services_from_persistence[1]
        for key in service1_data.keys():
            assert getattr(service2, key) == getattr(service2_from_persistence,
                                                     key)

    def test_modify(self, table, host_repo, service_repo,
                    host_data, service1_data, service2_data):
        host_repo.add(Host(**host_data))
        host_from_persistence = host_repo.all()[0]
        service = Service(**service1_data)
        service_repo.add(host_from_persistence.id, service)
        service_from_persistence = host_repo.all()[0].services[0]

        modified_service = Service(**service2_data)
        modified_service.id = service_from_persistence.id
        service_repo.modify(host_from_persistence.id, modified_service)

        services_from_persistence = host_repo.all()[0].services
        assert len(services_from_persistence) == 1
        modified_service_from_persistence = services_from_persistence[0]
        for key in (list(service2_data.keys()) + ['id']):
            assert getattr(modified_service, key) == getattr(
                modified_service_from_persistence, key)

    def test_delete(self, table, host_repo, service_repo,
                    host_data, service1_data, service2_data):
        host_repo.add(Host(**host_data))
        service = Service(**service1_data)
        service_repo.add(host_repo.all()[0].id, service)
        service_id = host_repo.all()[0].services[0].id
        service_repo.delete(service_id)
        assert len(host_repo.all()[0].services) == 0
