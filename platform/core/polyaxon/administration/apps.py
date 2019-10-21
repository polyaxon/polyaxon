from django.apps import AppConfig


class AdministrationConfig(AppConfig):
    name = 'administration'
    verbose_name = 'administration'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_admin_service()
