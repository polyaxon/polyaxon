# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings


def get_project_outputs_path(project_name):
    values = project_name.split('.')
    return os.path.join(settings.UPLOAD_ROOT, '/'.join(values))


def get_experiment_group_outputs_path(experiment_group_name):
    values = experiment_group_name.split('.')
    return os.path.join(settings.UPLOAD_ROOT, '/'.join(values))
