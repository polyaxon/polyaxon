# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models
from django.utils.functional import cached_property

from polyaxon_schemas.polyaxonfile.specification import GroupSpecification

from libs.blacklist import validate_blacklist_name
from libs.models import DiffModel, DescribableModel
from libs.spec_validation import validate_spec_content
from spawner.utils.constants import ExperimentLifeCycle


class Project(DiffModel, DescribableModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    name = models.CharField(
        max_length=256,
        validators=[validate_slug, validate_blacklist_name])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='projects')
    is_public = models.BooleanField(
        default=True,
        help_text='If project is public or private.')
    has_tensorboard = models.BooleanField(
        default=False,
        help_text='If project has a tensorboard.')
    has_notebook = models.BooleanField(
        default=False,
        help_text='If project has a notebook.')

    def __str__(self):
        return self.unique_name

    class Meta:
        unique_together = (('user', 'name'),)

    @property
    def unique_name(self):
        return '{}.{}'.format(self.user.username, self.name)

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
    sequence = models.IntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this group within the project.',)
    content = models.TextField(
        help_text='The yaml content of the polyaxonfile/specification.',
        validators=[validate_spec_content])
    project = models.ForeignKey(
        Project,
        related_name='experiment_groups',
        help_text='The project this polyaxonfile belongs to.')

    class Meta:
        ordering = ['sequence']
        unique_together = (('project', 'sequence'),)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last = ExperimentGroup.objects.filter(project=self.project).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(ExperimentGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.unique_name

    @property
    def unique_name(self):
        return '{}.{}'.format(self.project.unique_name, self.sequence)

    @cached_property
    def specification(self):
        return GroupSpecification.read(self.content)

    @cached_property
    def concurrency(self):
        if self.specification.settings:
            return self.specification.settings.concurrent_experiments
        return 1

    @cached_property
    def search_method(self):
        if self.specification.settings:
            return self.specification.settings.search_method
        return None

    @property
    def scheduled_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.SCHEDULED).distinct()

    @property
    def succeeded_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.SUCCEEDED).distinct()

    @property
    def failed_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.FAILED).distinct()

    @property
    def stopped_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.DELETED).distinct()

    @property
    def pending_experiments(self):
        return self.experiments.filter(
            experiment_status__status=ExperimentLifeCycle.CREATED).distinct()

    @property
    def running_experiments(self):
        return self.experiments.filter(
            experiment_status__status__in=ExperimentLifeCycle.RUNNING_STATUS).distinct()

    @property
    def n_experiments_to_start(self):
        """ We need to check if we are allowed to start the experiment
        If the polyaxonfile has concurrency we need to check how many experiments are running.
        """
        return self.concurrency - len(self.running_experiments)
