import logging

from hestia.signal_decorators import ignore_raw, ignore_updates, ignore_updates_pre

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import conf

from db.models.build_jobs import BuildJob
from libs.repos.utils import assign_build_code_reference
from lifecycles.jobs import JobLifeCycle
from options.registry.build_jobs import BUILD_JOBS_BACKEND
from signals.backend import set_backend
from signals.names import set_name
from signals.tags import set_tags

_logger = logging.getLogger('polyaxon.signals.build_jobs')


@receiver(pre_save, sender=BuildJob, dispatch_uid="build_job_pre_save")
@ignore_updates_pre
@ignore_raw
def build_job_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    set_tags(instance=instance)
    set_backend(instance=instance, default_backend=conf.get(BUILD_JOBS_BACKEND))
    assign_build_code_reference(instance)
    set_name(instance=instance, query=BuildJob.all)


@receiver(post_save, sender=BuildJob, dispatch_uid="build_job_post_save")
@ignore_updates
@ignore_raw
def build_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)
