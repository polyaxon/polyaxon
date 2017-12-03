# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings

from polyaxon_schemas.utils import TaskType

from api.celery_api import app as celery_app
from api.settings import CeleryTasks
from libs.redis_db import RedisExperimentStatus
from spawner import K8SSpawner
from spawner.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.tasks.experiments')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START)
def start_experiment(experiment_id):
    from experiments.models import Experiment, ExperimentStatus, ExperimentJob

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        logger.info('Experiment id `{}` does not exist'.format(experiment_id))
        return

    # Update experiment status to show that its started
    ExperimentStatus.objects.create(experiment=experiment, status=ExperimentLifeCycle.SCHEDULED)

    # Use spawner to start the experiment
    spawner = K8SSpawner(project_uuid=experiment.project.uuid.hex,
                         spec_uuid=experiment.spec.uuid.hex if experiment.spec else '',
                         experiment_uuid=experiment.uuid.hex,
                         specification=experiment.config,
                         k8s_config=settings.K8S_CONFIG,
                         namespace=settings.K8S_NAMESPACE,
                         in_cluster=True,
                         use_sidecar=True,
                         sidecar_config='')  # Use current settings config
    resp = spawner.start_experiment()

    # Get the number of jobs this experiment started
    master = resp[TaskType.MASTER]
    job_uuid = master['labels']['task_id']
    ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=master)
    for worker in resp[TaskType.WORKER]:
        job_uuid = worker['labels']['task_id']
        ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=worker)
    for ps in resp[TaskType.PS]:
        job_uuid = ps['labels']['task_id']
        ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=ps)

    # Add the experiment to the list of experiments to monitor
    RedisExperimentStatus.monitor(experiment.uuid.hex)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_CHECK_STATUS)
def check_experiment_status(experiment_id):
    from experiments.models import Experiment
    from libs.redis_db import RedisExperimentStatus

    experiment = Experiment.objects.get(id=experiment_id)
    status = experiment.calculated_status
    RedisExperimentStatus.set_status(experiment_uuid=experiment.uuid.hex, status=status)
