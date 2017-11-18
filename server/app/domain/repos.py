from abc import ABCMeta, abstractmethod

from .entities import Admin, Host, Service


class AdminRepo(metaclass=ABCMeta):
    @abstractmethod
    def get(self):
        r"""

        :return:
        :rtype: Admin
        """
        pass

    @abstractmethod
    def set(self, admin: Admin):
        pass


class HostRepo(metaclass=ABCMeta):
    @abstractmethod
    def next_identity(self):
        pass

    @abstractmethod
    def save(self, host: Host):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def all(self):
        r"""

        :return:
        :rtype: list of Host
        """
        pass


class ServiceRepo(metaclass=ABCMeta):
    @abstractmethod
    def next_identity(self):
        pass

    @abstractmethod
    def save(self, host_id, service: Service):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class RepoFactory(object):
    def __init__(self):
        pass

    def build(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


repos = RepoFactory()
