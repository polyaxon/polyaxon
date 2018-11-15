# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.cli.getters.project import get_project_or_local
from polyaxon_cli.managers.experiment import ExperimentManager
from polyaxon_cli.managers.experiment_job import ExperimentJobManager


def get_experiment_or_local(experiment=None):
    return experiment or ExperimentManager.get_config_or_raise().id


def get_project_experiment_or_local(project=None, experiment=None):
    user, project_name = get_project_or_local(project)
    experiment = get_experiment_or_local(experiment)
    return user, project_name, experiment


def get_experiment_job_or_local(job=None):
    return job or ExperimentJobManager.get_config_or_raise().id
