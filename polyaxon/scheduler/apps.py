from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = 'Scheduler'

    def ready(self):
        import signals.build_jobs  # noqa
        import signals.experiments  # noqa
        import signals.experiment_groups  # noqa
        import signals.jobs  # noqa
        import signals.projects  # noqa
        import signals.project_notebook_jobs  # noqa
        import signals.project_tensorboard_jobs  # noqa
        import signals.nodes  # noqa
