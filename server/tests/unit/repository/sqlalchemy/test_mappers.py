from datetime import datetime
import pytest

from app.repository.sqlalchemy.mappers import admin_model_2_admin, \
    admin_2_admin_model, service_2_service_model, service_model_2_service, \
    host_2_host_model, host_model_2_host
from app.repository.sqlalchemy.models import AdminModel, ServiceModel, HostModel
from app.domain.entities import Admin, Service, Host

time = datetime.now()


class TestAdminMapper(object):
    @pytest.fixture
    def admin_data(self):
        return {
            'username': 'test',
            'original_password': '123',
            'sign': 'Are u handsome?',
            'tip': 'Absolutely',
            'updated_at': time
        }

    @pytest.fixture
    def admin_model_data(self):
        return {
            'username': 'test',
            'password': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3',
            'sign': 'Are u handsome?',
            'tip': 'Absolutely',
            'updated_at': time
        }

    def test_entity_to_model(self, admin_data, admin_model_data):
        admin = Admin(**admin_data)
        admin_model = AdminModel(**admin_model_data)
        converted = admin_2_admin_model(admin)
        for key in admin_model_data.keys():
            assert getattr(converted, key) == getattr(admin_model, key)

    def test_model_to_entity(self, admin_data, admin_model_data):
        admin = Admin(**admin_data)
        admin_model = AdminModel(**admin_model_data)
        converted = admin_model_2_admin(admin_model)
        for key in ('username', 'password', 'sign', 'tip', 'updated_at'):
            assert getattr(converted, key) == getattr(admin, key)


class TestServiceMapper(object):
    @pytest.fixture
    def service_data(self):
        return {'id': 'fake_id1', 'name': 'nginx', 'detail': 'nginx service',
                'port': 80}

    def test_entity_to_model(self, service_data):
        service = Service(**service_data)
        service_model = ServiceModel(**service_data)
        converted = service_2_service_model(service, 1)
        for key in service_data.keys():
            assert getattr(converted, key) == getattr(service_model, key)
        assert converted.host_id == 1

    def test_model_to_entity(self, service_data):
        service = Service(**service_data)
        service_model = ServiceModel(**service_data)
        converted = service_model_2_service(service_model)
        for key in service_data.keys():
            assert getattr(converted, key) == getattr(service, key)


class TestHost(object):
    @pytest.fixture
    def service_data(self):
        return {'id': 'fake_id1', 'name': 'nginx', 'detail': 'nginx service',
                'port': 80}

    @pytest.fixture
    def host_data(self):
        return {'id': 'fake_id1', 'name': 'localhost', 'detail': 'this machine',
                'address': '127.0.0.1'}

    def test_entity_to_model(self, service_data, host_data):
        service = Service(**service_data)
        service_model = ServiceModel(**service_data)
        host = Host(**host_data, services=[service])
        host_model = HostModel(**host_data, services=[service_model])
        converted = host_2_host_model(host)
        for key in host_data.keys():
            assert getattr(converted, key) == getattr(host_model, key)
        assert len(converted.services) == 1
        for key in service_data.keys():
            assert getattr(converted.services[0], key) == getattr(service_model,
                                                                  key)

    def test_model_to_entity(self, service_data, host_data):
        service = Service(**service_data)
        service_model = ServiceModel(**service_data)
        host = Host(**host_data, services=[service])
        host_model = HostModel(**host_data, services=[service_model])
        converted = host_model_2_host(host_model)
        for key in host_data.keys():
            assert getattr(converted, key) == getattr(host, key)
        assert len(converted.services) == 1
        for key in service_data.keys():
            assert getattr(converted.services[0], key) == getattr(service, key)
