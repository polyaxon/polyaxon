# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.core.management.base import BaseCommand


class BaseMonitorCommand(BaseCommand):
    help = 'Watch namespace warning and errors events.'

    def add_arguments(self, parser):
        parser.add_argument('--log_sleep_interval',
                            type=int,
                            default=1)
        parser.add_argument('--persist',
                            default=False,
                            help='Persist collected events.', )
