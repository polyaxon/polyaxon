import logging

from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.experiment_groups import ExperimentGroup
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import CloningStrategy, Experiment, ExperimentMetric, ExperimentStatus
from event_manager.events.experiment import (
    EXPERIMENT_DELETED,
    EXPERIMENT_FAILED,
    EXPERIMENT_NEW_METRIC,
    EXPERIMENT_NEW_STATUS,
    EXPERIMENT_STOPPED,
    EXPERIMENT_SUCCEEDED
)
from libs.decorators import check_specification, ignore_raw, ignore_updates, ignore_updates_pre
from libs.paths.experiments import (
    create_experiment_logs_path,
    delete_experiment_logs,
    delete_experiment_outputs
)
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

logger = logging.getLogger('polyaxon.signals.experiments')


@receiver(pre_save, sender=Experiment, dispatch_uid="experiment_pre_save")
@ignore_updates_pre
@ignore_raw
def add_experiment_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    # Check if declarations need to be set
    if not instance.declarations and instance.specification:
        instance.declarations = instance.specification.declarations

    # Add code reference
    # Check if :
    # the experiment is new
    # that it has an exec section
    # that it's not cloned
    # that is not an external repo (because we did not clone it yet)
    # if the instance has a primary key then is getting updated
    condition = (
        not instance.specification or
        not instance.specification.run_exec or
        instance.specification.run_exec.git or
        instance.code_reference or
        not instance.project.has_code)
    if condition:
        return

    assign_code_reference(instance)


@receiver(post_save, sender=Experiment, dispatch_uid="experiment_saved")
@ignore_updates
@ignore_raw
def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(ExperimentLifeCycle.CREATED)

    # Clean outputs and logs
    delete_experiment_logs(instance.unique_name)
    delete_experiment_outputs(instance.unique_name)

    # Create logs path
    create_experiment_logs_path(instance.unique_name)


@receiver(pre_delete, sender=Experiment, dispatch_uid="experiment_deleted")
@ignore_raw
def experiment_pre_deleted(sender, **kwargs):
    instance = kwargs['instance']
    # Delete outputs and logs
    delete_experiment_outputs(instance.unique_name)
    delete_experiment_logs(instance.unique_name)

    # Delete clones
    for experiment in instance.clones.filter(cloning_strategy=CloningStrategy.RESUME):
        experiment.delete()


@receiver(post_delete, sender=Experiment, dispatch_uid="experiment_deleted")
@ignore_raw
def experiment_post_deleted(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=EXPERIMENT_DELETED, instance=instance)


@receiver(post_save, sender=ExperimentJob, dispatch_uid="experiment_job_saved")
@ignore_updates
@ignore_raw
def new_experiment_job(sender, **kwargs):
    instance = kwargs['instance']
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

    celery_app.send_task(
        SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS,
        kwargs={'experiment_id': experiment.id})


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="experiment_status_saved")
@ignore_raw
def new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)
    experiment = instance.experiment
    previous_status = experiment.last_status

    if created:
        # update experiment last_status
        experiment.experiment_status = instance
        experiment.save()
        auditor.record(event_type=EXPERIMENT_NEW_STATUS,
                       instance=experiment,
                       previous_status=previous_status)

    if instance.status == ExperimentLifeCycle.SUCCEEDED:
        # update all workers with succeeded status, since we will trigger a stop mechanism
        for job in experiment.jobs.all():
            if not job.is_done:
                job.set_status(JobLifeCycle.SUCCEEDED, message='Master is done.')
        auditor.record(event_type=EXPERIMENT_SUCCEEDED,
                       instance=experiment,
                       previous_status=previous_status)
    if instance.status == ExperimentLifeCycle.FAILED:
        auditor.record(event_type=EXPERIMENT_FAILED,
                       instance=experiment,
                       previous_status=previous_status)

    if instance.status == ExperimentLifeCycle.STOPPED:
        auditor.record(event_type=EXPERIMENT_STOPPED,
                       instance=experiment,
                       previous_status=previous_status)


@receiver(post_save, sender=ExperimentMetric, dispatch_uid="experiment_metric_saved")
@ignore_updates
@ignore_raw
def new_experiment_metric(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    # update experiment last_metric
    experiment.experiment_metric = instance
    experiment.save()
    auditor.record(event_type=EXPERIMENT_NEW_METRIC,
                   instance=experiment)


@receiver(post_save, sender=Experiment, dispatch_uid="start_new_experiment")
@check_specification
@ignore_updates
@ignore_raw
def start_new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    if instance.is_independent:
        # Start building the experiment and then Schedule it to be picked by the spawners
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_BUILD,
            kwargs={'experiment_id': instance.id},
            countdown=1)


@receiver(pre_delete, sender=Experiment, dispatch_uid="stop_running_experiment")
@check_specification
@ignore_raw
def stop_running_experiment(sender, **kwargs):
    from scheduler import experiment_scheduler
    instance = kwargs['instance']
    try:
        _ = instance.experiment_group  # noqa
        # Delete all jobs from DB before sending a signal to k8s,
        # this way no constants will be updated in the meanwhile
        instance.jobs.all().delete()
        experiment_scheduler.stop_experiment(instance, update_status=False)
    except ExperimentGroup.DoesNotExist:
        # The experiment was already stopped when the group was deleted
        pass


@receiver(post_save, sender=ExperimentStatus, dispatch_uid="handle_new_experiment_status")
@ignore_raw
def handle_new_experiment_status(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    if not experiment.specification:
        return

    if instance.status in (ExperimentLifeCycle.FAILED, ExperimentLifeCycle.SUCCEEDED):
        logger.info('One of the workers failed or Master for experiment `%s` is done, '
                    'send signal to other workers to stop.', experiment.unique_name)
        # Schedule stop for this experiment because other jobs may be still running
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={'experiment_id': experiment.id,
                    'update_status': False})
