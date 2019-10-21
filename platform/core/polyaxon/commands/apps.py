from django.apps import AppConfig


class CommandsConfig(AppConfig):
    name = 'commands'
    verbose_name = 'Commands'

    def ready(self):
        import signals.users  # noqa
        import signals.deletion  # noqa
