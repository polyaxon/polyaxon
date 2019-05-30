from typing import Any

from hestia.service_interface import Service

from conf.conf_manager import conf_cache_manager
from conf.exceptions import ConfException
from conf.handlers.settings_handler import SettingsHandler
from conf.option_manager import option_manager
from options.option import OptionStores


class ConfService(Service):
    __all__ = ('get', 'set', 'delete')

    option_manager = option_manager
    cache_manager = conf_cache_manager

    def __init__(self):
        self.stores = {}

    def get_options_handler(self):
        return None

    def can_handle(self, key: str) -> bool:
        return isinstance(key, str) and self.option_manager.knows(key=key)

    def get_option(self, key: str,) -> 'Option':
        return self.option_manager.get(key=key)

    def get_store(self, option: 'Option') -> Any:
        if option.store not in self.stores:
            raise ConfException('Option `{}` has an invalid store.'.format(option.key))

        return self.stores[option.store]

    def get(self, key: str) -> Any:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException('Conf service request an unknown key `{}`.'.format(key))

        value = self.cache_manager.get_from_cache(key=key)
        if self.cache_manager.is_valid_value(value=value):
            return value

        option = self.get_option(key=key)
        store = self.get_store(option=option)
        return store.get(option=option)

    def set(self, key: str, value: Any) -> None:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException('Conf service request an unknown key `{}`.'.format(key))
        if value is None:
            raise ConfException('Conf service requires a value for key `{}` to set.'.format(key))

        option = self.get_option(key=key)
        store = self.get_store(option=option)
        store.set(option=option, value=value)

    def delete(self, key: str) -> None:
        if not self.is_setup:
            return
        if not self.can_handle(key=key):
            raise ConfException('Conf service request an unknown key `{}`.'.format(key))

        option = self.get_option(key=key)
        store = self.get_store(option=option)
        store.delete(option=option)

    def setup(self) -> None:
        super().setup()
        # Load default options
        import conf.options  # noqa

        self.stores[OptionStores.SETTINGS] = SettingsHandler()

        options_handler = self.get_options_handler()
        if options_handler:
            self.stores[OptionStores.DB_OPTION] = options_handler
