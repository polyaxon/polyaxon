# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks, Intervals
from api.celery_api import app as celery_app
from experiments.tasks import build_experiment
from projects.models import PolyaxonSpec

logger = logging.getLogger('polyaxon.tasks.projects')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START_GROUP, bind=True)
def start_group_experiments(task, spec_id):

    try:
        polyaxon_spec = PolyaxonSpec.objects.get(id=spec_id)
    except PolyaxonSpec.DoesNotExist:
        logger.info('PolyaxonSpec `{}` does not exist anymore.'.format(spec_id))
        return

    pending_experiments = list(polyaxon_spec.pending_experiments.values_list('id', flat=True))
    experiment_to_start = polyaxon_spec.n_experiments_to_start
    while experiment_to_start > 0 and pending_experiments:
        experiment_id = pending_experiments.pop()
        build_experiment.delay(experiment_id=experiment_id)
        experiment_to_start -= 1

    if pending_experiments:
        # Schedule another task
        task.apply_async(spec_id, countdown=Intervals.EXPERIMENTS_SCHEDULER)

