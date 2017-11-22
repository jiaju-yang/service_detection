class RepoFactory(object):
    def __init__(self):
        pass

    def build(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


repos = RepoFactory()
