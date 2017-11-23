from app.domain.entities import Admin, Host, Service
from .models import AdminModel, HostModel, ServiceModel


def _extract_properties(o, *properties):
    result = {}
    for property in properties:
        if isinstance(property, str):
            result[property] = getattr(o, property)
        elif isinstance(property, (list, tuple)):
            result[property[1]] = getattr(o, property[0])
        else:
            raise TypeError()
    return result


def admin_model_2_admin(admin_model: AdminModel):
    return Admin(
        **_extract_properties(admin_model, 'username', 'updated_at', 'sign',
                             'tip', ('password', 'encrypted_password')))


def admin_2_admin_model(admin: Admin):
    return AdminModel(**_extract_properties(
        admin, 'username', 'password', 'updated_at', 'sign', 'tip'))


def service_model_2_service(service_model: ServiceModel):
    return Service(
        **_extract_properties(service_model, 'id', 'name', 'detail', 'port'))


def service_2_service_model(service: Service, host_id):
    return ServiceModel(**_extract_properties(
        service, 'id', 'name', 'detail', 'port'), host_id=host_id)


def host_model_2_host(host_model: HostModel):
    return Host(**_extract_properties(
        host_model, 'id', 'name', 'detail', 'address'),
                services=[service_model_2_service(service) for service in
                          host_model.services])


def host_2_host_model(host: Host):
    return HostModel(**_extract_properties(
        host, 'id', 'name', 'detail', 'address'),
                     services=[service_2_service_model(service, host.id) for
                               service in
                               host.services])
