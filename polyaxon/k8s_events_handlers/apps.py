from django.apps import AppConfig


class K8SEventsHandlersConfig(AppConfig):
    name = 'k8s_events_handlers'
    verbose_name = 'K8SEventsHandlers'

    def ready(self):
        import signals.statuses  # noqa
        import signals.deletion  # noqa
