from .repos import AdminRepo, ServiceRepo, HostRepo
from . import usecases


def inject_repos(*, admin: AdminRepo = None, host: HostRepo = None,
                 service: ServiceRepo = None):
    usecases.admin_repo = admin
    usecases.host_repo = host
    usecases.service_repo = service
