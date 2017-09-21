from .models import AdminModel, HostModel
from .domain.entities import Admin, Host


def admin_model_2_admin(admin_model: AdminModel):
    return Admin(admin_model.username, admin_model.password,
                 admin_model.updated_at, admin_model.sign, admin_model.tip)


def admin_2_admin_model(admin: Admin):
    return AdminModel(admin.username, admin.password, admin.updated_at,
                      admin.sign, admin.tip)


def host_model_2_host(host_model:HostModel):
    return Host()