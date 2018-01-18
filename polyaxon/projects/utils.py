# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings

from libs.outputs import delete_outputs


def get_project_data_path(project_name):
    return os.path.join(settings.DATA_ROOT, project_name.replace('.', '/'))


def get_project_outputs_path(project_name):
    return os.path.join(settings.OUTPUTS_ROOT, project_name.replace('.', '/'))


def get_experiment_group_outputs_path(experiment_group_name):
    return os.path.join(settings.OUTPUTS_ROOT, experiment_group_name.replace('.', '/'))


def delete_project_outputs(project_name):
    path = get_project_outputs_path(project_name)
    delete_outputs(path)


def delete_experiment_group_outputs(experiment_group_name):
    path = get_project_outputs_path(experiment_group_name)
    delete_outputs(path)
