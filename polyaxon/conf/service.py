from typing import Any

from hestia.service_interface import Service

from conf.exceptions import ConfException


class ConfService(Service):
    __all__ = ('get', 'set', 'delete',)

    def __init__(self):
        self._settings = None

    def get(self, key: str) -> Any:
        if hasattr(self._settings, key):
            return getattr(self._settings, key)
        else:
            raise ConfException(
                'The configuration option `{}` was not found or not correctly set.'.format(key))

    def set(self, name: str, value: Any) -> None:
        setattr(self._settings, name, value)

    def delete(self, name: str) -> None:
        delattr(self._settings, name)

    def setup(self) -> None:
        super().setup()
        from django.conf import settings

        self._settings = settings
