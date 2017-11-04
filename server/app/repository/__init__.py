from app.domain.repos import repo_factory


def build(app):
    repo_config = RepoConfig(app)
    repos = repo_config.get_repos()
    repo_factory.build(**repos)


def init(app):
    repo_config = RepoConfig(app)
    repo_config.init()


class RepoConfig(object):
    def __init__(self, app):
        engine_type = app.config['DB']
        if engine_type == 'sqlalchemy':
            from .sqlalchemy import init, get_repos
        else:
            raise NotImplementedError()
        self.init = lambda: init(app)
        self.get_repos = lambda: get_repos(app)


__all__ = ['build', 'init']
