# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from experiments.models import Experiment


def is_experiment_still_running(experiment_id=None, experiment_uuid=None):
    if not any([experiment_id, experiment_uuid]) or all([experiment_id, experiment_uuid]):
        raise ValueError('`is_experiment_still_running` function expects an experiment id or uuid.')

    try:
        if experiment_uuid:
            experiment = Experiment.objects.get(uuid=experiment_uuid)
        else:
            experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        return False

    if not experiment.is_running:
        return False

    return True
