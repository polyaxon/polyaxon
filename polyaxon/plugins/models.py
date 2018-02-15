# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from polyaxon_schemas.polyaxonfile.specification import PluginSpecification

from libs.models import DiffModel
from libs.spec_validation import validate_tensorboard_spec_content

logger = logging.getLogger('polyaxon.plugins')


class PluginJobBase(DiffModel):
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


class TensorboardJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""

    def __str__(self):
        if hasattr(self, 'project'):
            return '{} tensorboard<{}>'.format(self.project, self.image)
        logger.warning('Tensorboard with id `{}` is orphan.'.format(self.id))
        return self.image

    @cached_property
    def compiled_spec(self):
        return PluginSpecification(values=self.config)

    @cached_property
    def resources(self):
        return self.compiled_spec.total_resources

    @cached_property
    def image(self):
        return self.compiled_spec.run_exec.image


class NotebookJob(PluginJobBase):
    """A model that represents the configuration for tensorboard job."""

    def __str__(self):
        if hasattr(self, 'project'):
            return '{} notebook'.format(self.project)
        logger.warning('Notebook with id `{}` is orphan.'.format(self.id))
        return 'Notebook {}'.format(self.id)
