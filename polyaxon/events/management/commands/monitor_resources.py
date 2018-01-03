# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import time

from libs.utils import to_bool
from events.management.commands._base_monitor import BaseMonitorCommand
from events.monitors import resources


class Command(BaseMonitorCommand):
    help = 'Watch jobs/containers resources.'

    def handle(self, *args, **options):
        log_sleep_interval = options['log_sleep_interval']
        persist = to_bool(options['persist'])
        self.stdout.write(
            "Started a new resources monitor with, "
            "log sleep interval: `{}` and persist: `{}`".format(log_sleep_interval, persist),
            ending='\n')
        containers = {}
        while True:
            try:
                resources.run(containers, persist)
            except Exception as e:
                resources.logger.exception("Unhandled exception occurred %s\n" % e)

            time.sleep(log_sleep_interval)
