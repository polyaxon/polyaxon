from django.apps import AppConfig
from django.conf import settings


class APIConfig(AppConfig):
    name = 'api'
    verbose_name = 'API'

    def ready(self):
        from signals.experiments import *  # noqa
        from signals.experiment_groups import *  # noqa
        from signals.projects import *  # noqa
        from signals.project_plugin_jobs import *  # noqa
        from signals.nodes import *  # noqa
        from signals.repos import *  # noqa
        from api.users.signals import create_auth_token  # noqa
        if settings.AUTH_LDAP_ENABLED:
            from api.users.ldap_signals import populate_user_handler  # noqa
