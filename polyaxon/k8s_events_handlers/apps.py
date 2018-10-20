from django.apps import AppConfig


class K8SEventsHandlersConfig(AppConfig):
    name = 'k8s_events_handlers'
    verbose_name = 'K8SEventsHandlers'

    def ready(self):
        import signals.build_jobs  # noqa
        import signals.experiments  # noqa
        import signals.experiment_groups  # noqa
        import signals.jobs  # noqa
        import signals.projects  # noqa
        import signals.project_notebook_jobs  # noqa
        import signals.project_tensorboard_jobs  # noqa
        import signals.nodes  # noqa
        import signals.pipelines  # noqa
