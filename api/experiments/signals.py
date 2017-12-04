# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle


def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    from experiments.tasks import start_experiment

    instance.set_status(ExperimentLifeCycle.CREATED)
    if instance.is_independent:
        # Schedule the new experiment to be picked by the spawner
        start_experiment.delay(experiment_id=instance.id)


def new_experiment_job(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment job
    if not created:
        return

    from libs.redis_db import RedisExperimentJobStatus

    uuid = instance.uuid.hex
    RedisExperimentJobStatus.set_status(job_uuid=uuid, status=JobLifeCycle.CREATED)
    RedisExperimentJobStatus.monitor(uuid, instance.experiment.uuid.hex)


def new_experiment_job_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment job status
    if not created:
        return

    # Check if we need to change the experiment status
    experiment = instance.job.experiment
    if experiment.is_done:
        return

    from experiments.tasks import check_experiment_status

    check_experiment_status.delay(experiment_uuid=experiment.uuid.hex)
