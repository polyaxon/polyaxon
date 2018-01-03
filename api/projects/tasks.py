# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks, Intervals
from api.celery_api import app as celery_app
from experiments.tasks import build_experiment
from projects.models import ExperimentGroup

logger = logging.getLogger('polyaxon.tasks.projects')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START_GROUP, bind=True, max_retries=None)
def start_group_experiments(self, experiment_group_id):
    try:
        experiment_group = ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `{}` was not found.'.format(experiment_group_id))
        if self.request.retries < 2:
            logger.info('Trying again for ExperimentGroup `{}`.'.format(experiment_group_id))
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

        logger.info('Something went wrong, '
                    'the ExperimentGroup `{}` does not exist anymore.'.format(experiment_group_id))
        return

    pending_experiments = experiment_group.pending_experiments
    experiment_to_start = experiment_group.n_experiments_to_start
    while experiment_to_start > 0 and pending_experiments:
        experiment = pending_experiments.pop()
        build_experiment.delay(experiment_id=experiment.id)
        experiment_to_start -= 1

    if pending_experiments:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
