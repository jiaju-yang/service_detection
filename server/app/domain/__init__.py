from .repos import AdminRepo, ServiceRepo, HostRepo, repos


def inject_repos(*, admin: AdminRepo = None, host: HostRepo = None,
                 service: ServiceRepo = None):
    repos.build(**locals())
