from django.apps import AppConfig


class AccessConfig(AppConfig):
    name = 'access'
    verbose_name = 'access'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_access_service()
