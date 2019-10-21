from typing import Any

from django.db import InterfaceError, OperationalError, ProgrammingError

from conf.exceptions import ConfException
from conf.handler import BaseHandler


class ClusterOptionsHandler(BaseHandler):
    def __init__(self):
        self._model = None
        self._owner = None

    @property
    def owner(self) -> 'Owner':
        if self._owner:
            return self._owner

        from db.models.clusters import Cluster

        try:
            cluster = Cluster.load()
        except (Cluster.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            return None

        self._owner = cluster.get_or_create_owner(cluster)
        return self._owner

    @property
    def model(self):
        if self._model:
            return self._model

        from db.models.config_options import ConfigOption
        self._model = ConfigOption
        return self._model

    def get(self, option: 'Option') -> Any:
        try:
            config_option = self.model.objects.get(owner=self.owner, key=option.key)
            return config_option.secret if option.is_secret else config_option.value
        except (self.model.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            if not option.is_optional:
                raise ConfException(
                    'The configuration option `{}` was not found or '
                    'not correctly set.'.format(option.key))
            return option.default

    def set(self, option: 'Option', value: Any) -> None:
        try:
            config_option = self.model.objects.get(owner=self.owner, key=option.key)
            if option.is_secret:
                config_option.secret = value
                config_option.value = None  # Ensure we have always a correct state
            else:
                config_option.value = value
                config_option.secret = None  # Ensure we have always a correct state
            config_option.save()
        except (self.model.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            try:
                if option.is_secret:
                    self.model.objects.create(owner=self.owner, key=option.key, secret=value)
                else:
                    self.model.objects.create(owner=self.owner, key=option.key, value=value)
            except (InterfaceError, ProgrammingError, OperationalError):
                pass

    def delete(self, option: 'Option') -> None:
        try:
            config_option = self.model.objects.get(owner=self.owner, key=option.key)
            config_option.delete()
        except (self.model.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            pass
