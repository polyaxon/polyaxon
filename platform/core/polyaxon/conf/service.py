from conf.handlers.settings_handler import SettingsHandler
from conf.option_service import OptionService
from options.option import OptionStores


class ConfService(OptionService):
    service_name = 'Conf'

    def setup(self) -> None:
        super().setup()
        # Load default options
        import conf.options  # noqa

        self.stores[OptionStores.SETTINGS] = SettingsHandler()

        options_handler = self.get_options_handler()
        if options_handler:
            self.stores[OptionStores.DB_OPTION] = options_handler
