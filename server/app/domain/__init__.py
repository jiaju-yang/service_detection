from .repos import AdminRepo, ServiceRepo, HostRepo
from .registry import repos


def inject_repos(*, admin: AdminRepo = None, host: HostRepo = None,
                 service: ServiceRepo = None):
    for key, value in locals().items():
        if value:
            repos.build(**{key: value})
