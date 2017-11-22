import inspect

from app.domain.entities import Admin, Host, Service
from .models import AdminModel, HostModel, ServiceModel


def require_fields(o, keys):
    return {key: value for key, value in dict(inspect.getmembers(o)).items() if
            key in keys}


def admin_model_2_admin(admin_model: AdminModel):
    return Admin(**{**require_fields(
        admin_model, ('username', 'updated_at', 'sign', 'tip')),
                    **{'encrypted_password': admin_model.password}})


def admin_2_admin_model(admin: Admin):
    return AdminModel(**require_fields(
        admin, ('username', 'password', 'updated_at', 'sign', 'tip')))


def host_model_2_host(host_model: HostModel):
    return Host(**require_fields(
        host_model, ('id', 'name', 'detail', 'address')),
                services=[service_model_2_service(service) for service in
                          host_model.services])


def host_2_host_model(host: Host):
    return HostModel(**require_fields(
        host, ('id', 'name', 'detail', 'address')),
                     services=[service_2_service_model(service, host.id) for
                               service in
                               host.services])


def service_model_2_service(service_model: ServiceModel):
    return Service(**require_fields(
        service_model, ('id', 'name', 'detail', 'port')))


def service_2_service_model(service: Service, host_id):
    return ServiceModel(**require_fields(
        service, ('id', 'name', 'detail', 'port')), host_id=host_id)
