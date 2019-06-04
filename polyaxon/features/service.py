from conf.option_service import OptionService
from options.option import OptionStores


class FeaturesService(OptionService):
    service_name = 'Features'

    def setup(self) -> None:
        super().setup()
        # Load default options
        import conf.options  # noqa

        options_handler = self.get_options_handler()
        if options_handler:
            self.stores[OptionStores.DB_OPTION] = options_handler

