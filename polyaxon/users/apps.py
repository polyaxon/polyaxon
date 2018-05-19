from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Users'

    def ready(self):
        from users.signals import create_auth_token  # noqa
        if settings.AUTH_LDAP_ENABLED:
            from users.ldap_signals import populate_user_handler  # noqa
