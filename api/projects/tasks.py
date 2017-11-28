# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings

from api.settings import CeleryTasks
from api.celery_api import app as celery_app
from experiments.tasks import start_experiment

logger = logging.getLogger('polyaxon.api.experiments')


@celery_app.task(name=CeleryTasks.START_EXPERIMENTS, bind=True)
def start_group_experiments(task, spec_id):
    from projects.models import PolyaxonSpec

    try:
        polyaxon_spec = PolyaxonSpec.objects.get(id=spec_id)
    except PolyaxonSpec.DoesNotExist:
        # TODO : log
        return

    pending_experiments = list(polyaxon_spec.pending_experiments.values_list('id', flat=True))
    experiment_to_start = polyaxon_spec.n_experiments_to_start
    while experiment_to_start > 0 and pending_experiments:
        experiment_id = pending_experiments.pop()
        start_experiment.delay(experiment_id=experiment_id)

    if pending_experiments:
        # Schedule another task
        task.apply_async(spec_id, countdown=settings.EXPERIMENTS_SCHEDULER_INTERVAL_SEC)

