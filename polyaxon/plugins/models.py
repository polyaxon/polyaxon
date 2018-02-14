# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from polyaxon_schemas.polyaxonfile.specification import Specification

from libs.models import DiffModel
from libs.spec_validation import validate_tensorboard_spec_content


class TensorboardJob(DiffModel):
    """A model that represents the configuration for tensorboard job."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+')
    config = JSONField(
        help_text='The compiled polyaxonfile for tensorboard.',
        validators=[validate_tensorboard_spec_content])

    def __str__(self):
        if hasattr(self, 'project'):
            return '{}<{}>'.format(self.project, self.image)
        return self.image

    @cached_property
    def compiled_spec(self):
        return Specification(experiment='tensorboard', values=self.config)

    @cached_property
    def resources(self):
        return self.compiled_spec.total_resources

    @cached_property
    def image(self):
        return self.compiled_spec.run_exec.image
