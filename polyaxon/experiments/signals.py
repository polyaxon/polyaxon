# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from experiments.models import Experiment, ExperimentJob, ExperimentJobStatus, ExperimentStatus
from libs.decorators import ignore_raw
from projects.models import ExperimentGroup
from spawner import scheduler
from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle

from experiments.tasks import check_experiment_status, build_experiment


logger = logging.getLogger('polyaxon.experiments')


@receiver(post_save, sender=Experiment, dispatch_uid="experiment_saved")
@ignore_raw
def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    instance.set_status(ExperimentLifeCycle.CREATED)
    if instance.is_independent:
        # Start building the experiment and then Schedule it to be picked by the spawner
        build_experiment.delay(experiment_id=instance.id)


@receiver(pre_delete, sender=Experiment, dispatch_uid="experiment_deleted")
@ignore_raw
def experiment_deleted(sender, **kwargs):
    instance = kwargs['instance']
    try:
        _ = instance.experiment_group
        scheduler.stop_experiment(instance, update_status=False)
    except ExperimentGroup.DoesNotExist:
        # The experiment was already stopped when the group was deleted
        pass


@receiver(post_save, sender=ExperimentJob, dispatch_uid="experiment_job_saved")
@ignore_raw
def new_experiment_job(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment job
    if not created:
        return

    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=ExperimentJobStatus, dispatch_uid="experiment_job_status_saved")
@ignore_raw
def new_experiment_job_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # check if the new status is done to remove the containers from the monitors
    job = instance.job
    if job.is_done:
        from libs.redis_db import RedisJobContainers

        RedisJobContainers.remove_job(job.uuid.hex)

    # Check if the experiment job status
    if not created:
        return

    # Check if we need to change the experiment status
    experiment = instance.job.experiment
    if experiment.is_done:
        return

    check_experiment_status.delay(experiment_uuid=experiment.uuid.hex)


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="experiment_status_saved")
@ignore_raw
def new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']

    if instance.status in (ExperimentLifeCycle.FAILED, ExperimentLifeCycle.SUCCEEDED):
        logger.info('Master worker for experiment `{}` is done, '
                    'send signal to other workers to stop.'.format(instance.uuid.hex))
        # Schedule stop for this experiment because other jobs may be still running
        scheduler.stop_experiment(instance.experiment, update_status=False)
