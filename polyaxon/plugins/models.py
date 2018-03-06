# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from polyaxon_schemas.polyaxonfile.specification import PluginSpecification

from jobs.models import Job, JobStatus
from libs.spec_validation import validate_tensorboard_spec_content
from spawner.utils.constants import JobLifeCycle

logger = logging.getLogger('polyaxon.plugins')


class PluginJobBase(Job):
    """A base model for plugin jobs."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+')
    content = models.TextField(
        blank=True,
        null=True,
        help_text='The yaml content of the plugin polyaxonfile/specification.',
        validators=[validate_tensorboard_spec_content])
    config = JSONField(
        help_text='The compiled polyaxonfile for tensorboard.',
        validators=[validate_tensorboard_spec_content])

    class Meta:
        abstract = True

    @cached_property
    def compiled_spec(self):
        return PluginSpecification(values=self.config)

    @cached_property
    def resources(self):
        return self.compiled_spec.total_resources

    @cached_property
    def unique_name(self):
        return self.__str__()


class TensorboardJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""

    job_status = models.OneToOneField(
        'TensorboardJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True)

    def __str__(self):
        if hasattr(self, 'project'):
            return '{} tensorboard<{}>'.format(self.project, self.image)
        logger.warning('Tensorboard with id `{}` is orphan.'.format(self.id))
        return 'Tensorboard {}'.format(self.id)

    @cached_property
    def image(self):
        return self.compiled_spec.run_exec.image

    def set_status(self, status, message=None, details=None):
        return self._set_status(status_model=TensorboardJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class NotebookJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""

    job_status = models.OneToOneField(
        'NotebookJobStatus',
        related_name='+',
        blank=True,
        null=True,
        editable=True)

    def __str__(self):
        if hasattr(self, 'project'):
            return '{} notebook'.format(self.project)
        logger.warning('Notebook with id `{}` is orphan.'.format(self.id))
        return 'Notebook {}'.format(self.id)

    def set_status(self, status, message=None, details=None):
        return self._set_status(status_model=NotebookJobStatus,
                                logger=logger,
                                status=status,
                                message=message,
                                details=details)


class TensorboardJobStatus(JobStatus):
    """A model that represents tensorboard job status at certain time."""
    job = models.ForeignKey(TensorboardJob, related_name='statuses')


class NotebookJobStatus(JobStatus):
    """A model that represents notebook job status at certain time."""
    job = models.ForeignKey(NotebookJob, related_name='statuses')
