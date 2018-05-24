from django.core.management.base import BaseCommand


class BaseMonitorCommand(BaseCommand):
    help = 'Base events, resource, and errors monitor.'

    def add_arguments(self, parser):
        parser.add_argument('--log_sleep_interval',
                            type=int,
                            default=1)
        parser.add_argument('--persist',
                            default=False,
                            help='Persist collected events.', )
