from django.apps import AppConfig


class AuditorConfig(AppConfig):
    name = 'auditor'
    verbose_name = 'auditor'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_auditor_services()
