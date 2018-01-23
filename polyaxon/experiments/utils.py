# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings

from libs.outputs import delete_outputs


def get_experiment_outputs_path(experiment_name):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')
    return os.path.join(settings.OUTPUTS_ROOT, '/'.join(values))


def get_experiment_logs_path(experiment_name):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')
    return os.path.join(settings.LOGS_ROOT, '/'.join(values))


def delete_experiment_logs(experiment_group_name):
    path = get_experiment_logs_path(experiment_group_name)
    delete_outputs(path)


def delete_experiment_outputs(experiment_group_name):
    path = get_experiment_outputs_path(experiment_group_name)
    delete_outputs(path)
