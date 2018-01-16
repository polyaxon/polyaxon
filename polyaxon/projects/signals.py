# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from libs.decorators import ignore_raw
from projects.models import ExperimentGroup, Project
from projects.tasks import start_group_experiments
from experiments.models import Experiment
from spawner import scheduler


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
@ignore_raw
def new_experiment_group(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Parse polyaxonfile content and create the experiments
    specification = instance.specification
    for xp in range(specification.matrix_space):

        Experiment.objects.create(project=instance.project,
                                  user=instance.user,
                                  experiment_group=instance,
                                  config=specification.parsed_data[xp])

    start_group_experiments.apply_async((instance.id, ), countdown=1)


@receiver(pre_save, sender=ExperimentGroup, dispatch_uid="experiment_group_deleted")
@ignore_raw
def experiment_group_deleted(sender, **kwargs):
    """Stop all experiments before deleting the group."""

    instance = kwargs['instance']
    for experiment in instance.running_experiments:
        scheduler.stop_experiment(experiment, update_status=False)


@receiver(pre_delete, sender=Project, dispatch_uid="project_deleted")
@ignore_raw
def project_deleted(sender, **kwargs):
    instance = kwargs['instance']
    scheduler.stop_tensorboard(instance)
