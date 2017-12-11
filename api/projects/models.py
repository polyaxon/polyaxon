# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from polyaxon_schemas.polyaxonfile.specification import GroupSpecification

from libs.models import DiffModel, DescribableModel
from spawner.utils.constants import ExperimentLifeCycle


class Project(DiffModel, DescribableModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects')
    is_public = models.BooleanField(default=True, help_text='If project is public or private.')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('user', 'name'),)

    @property
    def has_code(self):
        return hasattr(self, 'repo')


class ExperimentGroup(DiffModel, DescribableModel):
    """A model that saves Specification/Polyaxonfiles."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experiment_groups')
    content = models.TextField(help_text='The yaml content of the polyaxonfile/specification.')
    project = models.ForeignKey(
        Project,
        related_name='experiment_groups',
        help_text='The project this polyaxonfile belongs to.')

    @cached_property
    def specification(self):
        return GroupSpecification.read(self.content)

    @cached_property
    def concurrency(self):
        if self.specification.settings:
            return self.specification.settings.conccurrent_experiments
        return 1

    @property
    def pending_experiments(self):
        return self.experiments.filter(status__status=ExperimentLifeCycle.CREATED)

    @property
    def running_experiments(self):
        return self.experiments.filter(status__status__in=ExperimentLifeCycle.RUNNING_STATUS)

    @property
    def n_experiments_to_start(self):
        """ We need to check if we are allowed to start the experiment
        If the polyaxonfile has concurrency we need to check how many experiments are running.
        """
        return self.concurrency - self.running_experiments.count()
