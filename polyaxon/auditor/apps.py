from django.apps import AppConfig


class AuditorConfig(AppConfig):
    name = 'auditor'
    verbose_name = 'auditor'

    def ready(self):
        from polyaxon.utils import config

        config.setup_services()
