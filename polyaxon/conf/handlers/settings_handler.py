from typing import Any

from conf.exceptions import ConfException
from conf.handler import BaseHandler


class SettingsHandler(BaseHandler):
    def __init__(self):
        from django.conf import settings

        self.settings = settings

    def get(self, option: 'Option') -> Any:
        if hasattr(self.settings, option.key):
            return getattr(self.settings, option.key)
        if not option.is_optional:
            raise ConfException(
                'The config option `{}` was not found or not correctly '
                'set on the settings backend.'.format(option.key))
        return option.default

    def set(self, option: 'Option', value: Any) -> None:
        raise ConfException(
            'The settings backend does not allow to set values, '
            'are you sure the key `{}` was correctly defined.'.format(option.key))

    def delete(self, option: 'Option') -> None:
        raise ConfException(
            'The settings backend does not allow to delete values, '
            'are you sure the key `{}` was correctly defined.'.format(option.key))
