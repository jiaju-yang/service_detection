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
    def add(self, host: Host):
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

    @abstractmethod
    def modify(self, host: Host):
        pass


class ServiceRepo(metaclass=ABCMeta):
    @abstractmethod
    def add(self, host_id, service: Service):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def modify(self, host_id, service: Service):
        pass


class RepoFactory(object):
    def __init__(self):
        self.admin, self.host, self.service = None, None, None

    def build(self, admin: AdminRepo, host: HostRepo, service: ServiceRepo):
        self.admin = admin
        self.host = host
        self.service = service


repo_factory = RepoFactory()
