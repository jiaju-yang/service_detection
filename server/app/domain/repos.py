from abc import ABCMeta, abstractmethod

from .entities import Admin, Host


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
