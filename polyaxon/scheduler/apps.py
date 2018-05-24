from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = 'Scheduler'

    def ready(self):
        pass
