import logging

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from experiments.clone import CloningStrategy
from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
    ExperimentStatus
)
from experiments.paths import (
    create_experiment_logs_path,
    delete_experiment_logs,
    delete_experiment_outputs
)
from experiments.statuses import ExperimentLifeCycle
from experiments.tasks import check_experiment_status
from jobs.statuses import JobLifeCycle
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from repos.utils import assign_code_reference

logger = logging.getLogger('polyaxon.experiments')


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
def experiment_deleted(sender, **kwargs):
    instance = kwargs['instance']
    # Delete outputs and logs
    delete_experiment_outputs(instance.unique_name)
    delete_experiment_logs(instance.unique_name)

    # Delete clones
    for experiment in instance.clones.filter(cloning_strategy=CloningStrategy.RESUME):
        experiment.delete()


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


@receiver(post_save, sender=ExperimentMetric, dispatch_uid="experiment_metric_saved")
@ignore_updates
@ignore_raw
def new_experiment_metric(sender, **kwargs):
    instance = kwargs['instance']
    experiment = instance.experiment
    # update experiment last_metric
    experiment.experiment_metric = instance
    experiment.save()
