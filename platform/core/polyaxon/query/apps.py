from django.apps import AppConfig


class QueryConfig(AppConfig):
    name = 'query'
    verbose_name = 'Query'

    def ready(self):
        from polyaxon.config_manager import config

        config.setup_query_service()
