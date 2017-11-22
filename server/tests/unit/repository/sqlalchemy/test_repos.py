from datetime import datetime

import pytest

from app.domain.entities import Admin, Host, Service
from app.domain.errors import NoAdministratorFound
from app.repository.sqlalchemy import (SqlalchemyAdminRepo, SqlalchemyHostRepo,
                                       SqlalchemyServiceRepo)
from app.repository.sqlalchemy.models import db
from tests.unit.utils import FlaskAppContextEnvironment


class DbEnvironment(FlaskAppContextEnvironment):
    @pytest.fixture
    def table(self, app_context):
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


class TestAdminRepoImpl(DbEnvironment):
    @pytest.fixture(scope='class')
    def repo(self):
        return SqlalchemyAdminRepo()

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
        return SqlalchemyHostRepo()

    @pytest.fixture
    def host1_data(self):
        return {'id': 'fake_id1', 'name': 'localhost', 'detail': 'this machine',
                'address': '127.0.0.1'}

    @pytest.fixture
    def host2_data(self):
        return {'id': 'fake_id2', 'name': 'server1',
                'detail': 'remote machine 1',
                'address': '8.8.8.8'}

    def test_next_identity(self, repo):
        new_id = repo.next_identity()
        assert type(new_id) is str

        next_new_id = repo.next_identity()
        assert new_id != next_new_id

    def test_save_one_host(self, table, repo, host1_data, host2_data):
        host = Host(**host1_data)
        repo.save(host)
        hosts_from_persistence = repo.all()
        assert len(hosts_from_persistence) == 1

        host_from_persistence = hosts_from_persistence[0]
        for key in host1_data.keys():
            assert getattr(host, key) == getattr(host_from_persistence, key)

    def test_save_multiple_host(self, table, repo, host1_data,
                                host2_data):
        hosts = [Host(**host1_data), Host(**host2_data)]
        for host in hosts:
            repo.save(host)
        hosts_from_persistence = repo.all()
        assert len(hosts) == 2

        for host, host_from_persistence in zip(hosts, hosts_from_persistence):
            for key in host1_data.keys():
                assert getattr(host, key) == getattr(host_from_persistence, key)

    def test_save_modified_host(self, table, repo, host1_data, host2_data):
        host = Host(**host1_data)
        repo.save(host)
        hosts_from_persistence = repo.all()
        assert len(hosts_from_persistence) == 1

        host.name, host.detail, host.address = host2_data['name'], host2_data[
            'detail'], host2_data['address']
        repo.save(host)
        hosts_from_persistence = repo.all()
        assert len(hosts_from_persistence) == 1

        host_from_persistence = hosts_from_persistence[0]
        for key in host2_data.keys():
            if key == 'id':
                assert host1_data['id'] == host_from_persistence.id
            else:
                assert host2_data[key] == getattr(host_from_persistence, key)

    def test_delete(self, table, repo, host1_data):
        host = Host(**host1_data)
        repo.save(host)
        repo.delete(repo.all()[0].id)
        assert len(repo.all()) == 0

    def test_query_by_id(self, table, repo, host1_data):
        host = Host(**host1_data)
        repo.save(host)
        saved_host = repo.host_of_id(host.id)
        for key in host1_data.keys():
            assert getattr(host, key) == getattr(saved_host, key)


class TestServiceRepoImpl(DbEnvironment):
    @pytest.fixture(scope='class')
    def host_repo(self):
        return SqlalchemyHostRepo()

    @pytest.fixture(scope='class')
    def service_repo(self):
        return SqlalchemyServiceRepo()

    @pytest.fixture
    def host_data(self):
        return {'id': 'fake_id', 'name': 'localhost', 'detail': 'this machine',
                'address': '127.0.0.1'}

    @pytest.fixture
    def service1_data(self):
        return {'id': 'fake_id1', 'name': 'nginx', 'detail': 'nginx service',
                'port': 80}

    @pytest.fixture
    def service2_data(self):
        return {'id': 'fake_id2', 'name': 'postgres',
                'detail': 'postgres database', 'port': 5432}

    def test_next_identity(self, service_repo):
        new_id = service_repo.next_identity()
        assert type(new_id) is str

        next_new_id = service_repo.next_identity()
        assert new_id != next_new_id

    def test_save_service(self, table, host_repo, service_repo,
                          host_data, service1_data, service2_data):
        host_repo.save(Host(**host_data))
        host_from_persistence = host_repo.all()[0]
        service1 = Service(**service1_data)
        service2 = Service(**service2_data)
        service_repo.save(host_from_persistence.id, service1)
        service_repo.save(host_from_persistence.id, service2)

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

    def test_save_modified_service(self, table, host_repo, service_repo,
                                   host_data, service1_data, service2_data):
        host_repo.save(Host(**host_data))
        host_from_persistence = host_repo.all()[0]
        service = Service(**service1_data)
        service_repo.save(host_from_persistence.id, service)
        assert len(host_repo.all()[0].services) == 1

        service.name, service.detail, service.port = service2_data['name'], \
                                                     service2_data['detail'], \
                                                     service2_data['port']
        service_repo.save(host_from_persistence.id, service)
        services_from_persistence = host_repo.all()[0].services
        assert len(services_from_persistence) == 1

        service_from_persistence = services_from_persistence[0]
        for key in service2_data.keys():
            if key == 'id':
                assert service1_data['id'] == service_from_persistence.id
            else:
                assert service2_data[key] == getattr(service_from_persistence,
                                                     key)

    def test_delete(self, table, host_repo, service_repo,
                    host_data, service1_data, service2_data):
        host_repo.save(Host(**host_data))
        service = Service(**service1_data)
        service_repo.save(host_repo.all()[0].id, service)
        service_id = host_repo.all()[0].services[0].id
        service_repo.delete(service_id)
        assert len(host_repo.all()[0].services) == 0
