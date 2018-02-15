# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from libs.decorators import ignore_raw
from projects.models import ExperimentGroup, Project
from projects.tasks import start_group_experiments
from experiments.models import Experiment
from projects.utils import (
    delete_project_outputs,
    delete_experiment_group_outputs,
    delete_project_logs,
    delete_experiment_group_logs,
    delete_project_repos,
)
from spawner import scheduler


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Clean outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)

    # Parse polyaxonfile content and create the experiments
    specification = instance.specification
    for xp in range(specification.matrix_space):
        Experiment.objects.create(project=instance.project,
                                  user=instance.user,
                                  experiment_group=instance,
                                  config=specification.parsed_data[xp])

    start_group_experiments.apply_async((instance.id,), countdown=1)


@receiver(pre_delete, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_deleted(sender, **kwargs):
    """Stop all experiments before deleting the group."""

    instance = kwargs['instance']
    for experiment in instance.running_experiments:
        # Delete all jobs from DB before sending a signal to k8s,
        # this way no statuses will be updated in the meanwhile
        experiment.jobs.all().delete()
        scheduler.stop_experiment(experiment, update_status=False)

    # Delete outputs and logs
    delete_experiment_group_outputs(instance.unique_name)
    delete_experiment_group_logs(instance.unique_name)


@receiver(post_save, sender=Project, dispatch_uid="project_saved")
@ignore_raw
def new_project(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)


@receiver(pre_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_deleted(sender, **kwargs):
    instance = kwargs['instance']
    scheduler.stop_tensorboard(instance)
    scheduler.stop_notebook(instance)
    # Delete tensorboard job
    if instance.tensorboard:
        instance.tensorboard.delete()

    # Delete notebook job
    if instance.notebook:
        instance.notebook.delete()

    # Clean outputs, logs, and repos
    delete_project_outputs(instance.unique_name)
    delete_project_logs(instance.unique_name)
    delete_project_repos(instance.unique_name)
