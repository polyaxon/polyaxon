from django.apps import AppConfig


class FeaturesConfig(AppConfig):
    name = 'features'
    verbose_name = 'Features'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_features_service()
