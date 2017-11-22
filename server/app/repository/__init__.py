def get(app):
    engine_type = app.config['DB']
    if engine_type == 'sqlalchemy':
        from .sqlalchemy import get_repos
    else:
        raise NotImplementedError()
    return get_repos(app)
