from django.apps import AppConfig


class OwnershipConfig(AppConfig):
    name = 'ownership'
    verbose_name = 'Ownership'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_ownership_service()
