from django.apps import AppConfig


class StoresConfig(AppConfig):
    name = 'stores'
    verbose_name = 'stores'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_stores_service()
