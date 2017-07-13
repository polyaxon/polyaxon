# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx


from api.settings import CeleryTasks
from api.celery import app
from core.models import Experiment


def start_experiment(experiment):
    # if experiment.is_running():
    #     return {'status': 'running'}

    execute.delay(experiment.id)
    return {'status': 'started'}


@app.task(name=CeleryTasks.START_EXPERIMENT)
def execute(experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        return

    plx_xp = plx.experiments.create_experiment(experiment.to_config())
    plx_xp.train()
