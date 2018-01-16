# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'
    verbose_name = 'Projects'

    def ready(self):
        from projects.signals import (
            new_experiment_group,
            experiment_group_deleted,
            project_deleted,
        )
