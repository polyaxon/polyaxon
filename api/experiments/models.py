# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from polyaxon_schemas.polyaxonfile.specification import Specification

from clusters.models import Cluster
from libs.models import DiffModel
from spawner.utils.constants import JobLifeCycle, ExperimentLifeCycle


class Experiment(DiffModel):
    """A model that represents experiments."""

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    cluster = models.ForeignKey(
        Cluster,
        related_name='experiments')
    project = models.ForeignKey(
        'projects.Project',
        related_name='experiments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='experiments')
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text='Name of the experiment')
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Description of the experiment.')
    spec = models.ForeignKey(
        'projects.PolyaxonSpec',
        blank=True,
        null=True,
        related_name='experiments',
        help_text='The polyaxon_spec that generate this experiment.')
    config = JSONField(
        # TODO: should be validated by the Specification validator
        help_text='The compiled polyaxon with specific values for this experiment.')
    original_experiment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='clones',
        help_text='The original experiment that was cloned from.')

    @cached_property
    def compiled_spec(self):
        return Specification(experiment=self.uuid, values=self.config)

    @property
    def last_job_statuses(self):
        """The statuses of the job in this experiment."""
        statuses = []
        for job in self.jobs.all():
            status = job.last_status
            if status is not None:
                statuses.append(status)
        return statuses

    @property
    def calculated_status(self):
        calculated_status = ExperimentLifeCycle.jobs_status(self.last_job_statuses)
        if calculated_status is None:
            return self.last_status
        return calculated_status

    @property
    def last_status(self):
        status = self.statuses.last()
        return status.status if status else None

    @property
    def is_running(self):
        return ExperimentLifeCycle.is_running(self.last_status)

    @property
    def is_done(self):
        return ExperimentLifeCycle.is_done(self.last_status)

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=ExperimentLifeCycle.DONE_STATUS).first()
        if status:
            return status.created_at
        return None

    @property
    def started_at(self):
        status = self.statuses.filter(status=ExperimentLifeCycle.STARTING).first()
        if status:
            return status.created_at
        return None

    @property
    def is_clone(self):
        return self.original_experiment is not None

    @property
    def is_independent(self):
        """If the experiment belongs to a polyaxon_spec or is independently created."""
        return not self.spec

    def update_status(self):
        current_status = self.last_status
        calculated_status = self.calculated_status
        if calculated_status != current_status:
            # Add new status to the experiment
            self.set_status(calculated_status)
            return True
        return False

    def set_status(self, status):
        ExperimentStatus.objects.create(experiment=self, status=status)


class ExperimentStatus(models.Model):
    """A model that represents an experiment status at certain time."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    experiment = models.ForeignKey(Experiment, related_name='statuses')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=ExperimentLifeCycle.CREATED,
        choices=ExperimentLifeCycle.CHOICES)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.status


class ExperimentMetric(models.Model):
    """A model that represents an experiment metric at certain time."""
    experiment = models.ForeignKey(Experiment, related_name='metrics')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    values = JSONField()

    class Meta:
        ordering = ['created_at']


class ExperimentJob(DiffModel):
    """A model that represents job related to an experiment"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    experiment = models.ForeignKey(Experiment, related_name='jobs')
    definition = JSONField(help_text='The specific values for this job.')

    @property
    def last_status(self):
        status = self.statuses.last()
        return status.status if status else None

    @property
    def is_running(self):
        return JobLifeCycle.is_running(self.last_status)

    @property
    def is_done(self):
        return JobLifeCycle.is_done(self.last_status)

    @property
    def started_at(self):
        status = self.statuses.filter(status=JobLifeCycle.BUILDING).first()
        if status:
            return status.created_at
        return None

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=JobLifeCycle.DONE_STATUS).last()
        if status:
            return status.created_at
        return None

    def set_status(self, status, message=None, details=None):
        current_status = self.last_status
        if status != current_status:
            # Add new status to the job
            ExperimentJobStatus.objects.create(job=self,
                                               status=status,
                                               message=message,
                                               details=details)
            return True
        return False


class ExperimentJobStatus(models.Model):
    """A model that represents job status at certain time."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    job = models.ForeignKey(ExperimentJob, related_name='statuses')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=JobLifeCycle.CREATED,
        choices=JobLifeCycle.CHOICES)

    message = models.CharField(max_length=256, null=True, blank=True)
    details = JSONField(null=True, blank=True, default={})

    def __str__(self):
        return self.status
