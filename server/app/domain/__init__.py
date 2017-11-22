from .repos import AdminRepo, ServiceRepo, HostRepo
from .registry import repos


def inject_repos(*, admin: AdminRepo = None, host: HostRepo = None,
                 service: ServiceRepo = None):
    repos.build(**locals())
