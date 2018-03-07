# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.apps import AppConfig


class PluginsConfig(AppConfig):
    name = 'plugins'
    verbose_name = 'Plugins'

    def ready(self):
        from plugins.signals import (
            new_tensorboard_job,
            new_notebook_job,
            new_tensorboard_job_status,
            new_notebook_job_status,
        )
