# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentStatus,
    ExperimentMetric,
)
from experiments.utils import delete_experiment_outputs, delete_experiment_logs, \
    create_experiment_logs_path
from libs.decorators import ignore_raw
from projects.models import ExperimentGroup
from spawner import scheduler
from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle

from experiments.tasks import check_experiment_status, build_experiment


logger = logging.getLogger('polyaxon.experiments')


@receiver(pre_save, sender=Experiment, dispatch_uid="experiment_saved")
@ignore_raw
def add_experiment_commit(sender, **kwargs):
    instance = kwargs['instance']

    # Check if :
    # the experiment is new
    # that it has an exec section
    # that it's not cloned
    # that is not an external repo (because we did not clone it yet)
    # if the instance has a primary key then is getting updated
    if (instance.pk or
            not instance.compiled_spec.run_exec or
            instance.compiled_spec.run_exec.git or
            instance.is_clone or
            not instance.project.has_code):
        return

    # Set the code commit to the experiment
    last_commit = instance.project.repo.last_commit
    if last_commit:
        instance.commit = last_commit[0]


@receiver(post_save, sender=Experiment, dispatch_uid="experiment_saved")
@ignore_raw
def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    instance.set_status(ExperimentLifeCycle.CREATED)

    # Create logs path
    create_experiment_logs_path(instance.unique_name)

    if instance.is_independent:
        # Start building the experiment and then Schedule it to be picked by the spawner
        build_experiment.apply_async((instance.id, ), countdown=1)


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

    delete_experiment_outputs(instance.unique_name)
    delete_experiment_logs(instance.unique_name)


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
    job = instance.job

    if created:
        # update job last_status
        job.job_status = instance
        job.save()

    # check if the new status is done to remove the containers from the monitors
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
    created = kwargs.get('created', False)
    experiment = instance.experiment

    if created:
        # update experiment last_status
        experiment.experiment_status = instance
        experiment.save()

    if instance.status == ExperimentLifeCycle.SUCCEEDED:
        # update all workers with succeeded status, since we will trigger a stop mechanism
        for job in experiment.jobs.all():
            if not job.is_done:
                job.set_status(JobLifeCycle.SUCCEEDED, message='Master is done.')

    if instance.status in (ExperimentLifeCycle.FAILED, ExperimentLifeCycle.SUCCEEDED):
        logger.info('One of the workers failed or Master for experiment `{}` is done, '
                    'send signal to other workers to stop.'.format(experiment.unique_name))
        # Schedule stop for this experiment because other jobs may be still running
        scheduler.stop_experiment(experiment, update_status=False)


@receiver(post_save, sender=ExperimentMetric, dispatch_uid="experiment_metric_saved")
@ignore_raw
def new_experiment_metric(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)
    experiment = instance.experiment

    if created:
        # update experiment last_metric
        experiment.experiment_metric = instance
        experiment.save()
