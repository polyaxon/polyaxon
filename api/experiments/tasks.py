# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import uuid

from django.conf import settings

from polyaxon_schemas.utils import TaskType

from api.utils import config
from api.celery_api import app as celery_app
from api.settings import CeleryTasks
from spawner import K8SSpawner
from spawner.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.tasks.experiments')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START)
def start_experiment(experiment_id):
    from experiments.models import Experiment, ExperimentJob

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        logger.info('Experiment id `{}` does not exist'.format(experiment_id))
        return

    # Update experiment status to show that its started
    experiment.set_status(ExperimentLifeCycle.SCHEDULED)

    # Use spawner to start the experiment
    spawner = K8SSpawner(project_uuid=experiment.project.uuid.hex,
                         spec_uuid=experiment.spec.uuid.hex if experiment.spec else '',
                         experiment_uuid=experiment.uuid.hex,
                         spec_config=experiment.config,
                         k8s_config=settings.K8S_CONFIG,
                         namespace=settings.K8S_NAMESPACE,
                         in_cluster=True,
                         use_sidecar=True,
                         sidecar_config=config.get_requested_params())
    resp = spawner.start_experiment()

    # Get the number of jobs this experiment started
    master = resp[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['task_id']
    job_uuid = uuid.UUID(job_uuid)
    ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=master)
    for worker in resp[TaskType.WORKER]:
        job_uuid = worker['pod']['metadata']['labels']['task_id']
        job_uuid = uuid.UUID(job_uuid)
        ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=worker)
    for ps in resp[TaskType.PS]:
        job_uuid = ps['pod']['metadata']['labels']['task_id']
        job_uuid = uuid.UUID(job_uuid)
        ExperimentJob.objects.create(uuid=job_uuid, experiment=experiment, definition=ps)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_CHECK_STATUS)
def check_experiment_status(experiment_uuid):
    from experiments.models import Experiment

    experiment = Experiment.objects.get(uuid=experiment_uuid)
    experiment.update_status()
