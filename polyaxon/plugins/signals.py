# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from libs.decorators import ignore_raw
from plugins.models import TensorboardJob, NotebookJob
from spawner.utils.constants import JobLifeCycle

logger = logging.getLogger('polyaxon.plugins')


@receiver(post_save, sender=TensorboardJob, dispatch_uid="tensorboard_job_saved")
@ignore_raw
def new_tensorboard_job(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment job
    if not created:
        return

    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=NotebookJob, dispatch_uid="notebook_job_saved")
@ignore_raw
def new_notebook_job(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment job
    if not created:
        return

    instance.set_status(status=JobLifeCycle.CREATED)
