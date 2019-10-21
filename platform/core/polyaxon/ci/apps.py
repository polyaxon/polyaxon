from django.apps import AppConfig


class CIConfig(AppConfig):
    name = 'ci'
    verbose_name = 'Continuous Integration'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_ci_service()
