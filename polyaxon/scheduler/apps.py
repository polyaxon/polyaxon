from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = 'Scheduler'

    def ready(self):
        import signals.experiments  # noqa
        import signals.experiment_groups  # noqa
        import signals.projects  # noqa
        import signals.project_plugin_jobs  # noqa
        import signals.nodes  # noqa
