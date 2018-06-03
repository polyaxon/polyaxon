from django.apps import AppConfig


class EventsHandlersConfig(AppConfig):
    name = 'events_handlers'
    verbose_name = 'EventsHandlers'

    def ready(self):
        import signals.build_jobs  # noqa
        import signals.experiments  # noqa
        import signals.experiment_groups  # noqa
        import signals.projects  # noqa
        import signals.project_plugin_jobs  # noqa
        import signals.nodes  # noqa
        import signals.pipelines  # noqa
