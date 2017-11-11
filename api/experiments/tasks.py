# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks
from api.celery_api import app
from experiments.task_status import ExperimentStatus

logger = logging.getLogger('polyaxon.api.experiments')


def get_experiment_run_status(experiment):
    job_id, status = ExperimentStatus.get_status(experiment.id)
    return {'job_id': job_id, 'status': status}


def start_experiment(experiment):
    job_id, status = ExperimentStatus.get_status(experiment.id)
    if not status or ExperimentStatus.is_final_status(status):
        job = execute.delay(experiment.id)
        ExperimentStatus.set_status(experiment.id, job.id, 'PENDING')
        return {'status': 'PENDING'}
    return {'status': status}


@app.task(name=CeleryTasks.START_EXPERIMENT)
def start_experiment(experiment_id):
    from experiments.models import Experiment

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        logger.info('Experiment id `{}` does not exist'.format(experiment_id))
        return

    # Update experiment status to show that its started
    # Use spawner to start the experiment
