# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings


def get_project_outputs_path(project_name):
    return os.path.join(settings.OUTPUTS_ROOT, project_name.replace('.', '/'))


def get_experiment_group_outputs_path(experiment_group_name):
    return os.path.join(settings.OUTPUTS_ROOT, experiment_group_name.replace('.', '/'))
