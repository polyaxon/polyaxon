# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from libs.models import DiffModel
from libs.resource_validation import validate_resource
from spawner.utils.constants import JobLifeCycle


class JobResources(models.Model):
    """A model that represents job resources."""
    cpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    memory = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])
    gpu = JSONField(
        null=True,
        blank=True,
        validators=[validate_resource])

    def __str__(self):
        def get_resource(resource, resource_name):
            if not resource:
                return ''
            return '{}: <{}-{}>'.format(resource_name,
                                        resource.get('requests'),
                                        resource.get('limits'))

        cpu = get_resource(self.cpu, 'CPU')
        memory = get_resource(self.memory, 'Memory')
        gpu = get_resource(self.gpu, 'GPU')
        resources = [cpu, memory, gpu]
        return ', '.join([r for r in resources if r])


class Job(DiffModel):
    class Meta:
        abstract = True

    @property
    def last_status(self):
        return self.job_status.status if self.job_status else None

    @property
    def is_running(self):
        return JobLifeCycle.is_running(self.last_status)

    @property
    def is_done(self):
        return JobLifeCycle.is_done(self.last_status)

    @property
    def started_at(self):
        status = self.statuses.filter(status=JobLifeCycle.BUILDING).first()
        if not status:
            status = self.statuses.filter(status=JobLifeCycle.RUNNING).first()
        if status:
            return status.created_at
        return None

    @property
    def finished_at(self):
        status = self.statuses.filter(status__in=JobLifeCycle.DONE_STATUS).last()
        if status:
            return status.created_at
        return None

    def _set_status(self, status_model, logger, status, message=None, details=None):
        current_status = self.last_status
        # We should not update statuses anymore
        if JobLifeCycle.is_done(current_status):
            logger.info(
                'Received a new status `{}` for job `{}`. '
                'But the job is already done with status `{}`'.format(
                    status, self.unique_name, current_status))
            return False
        if status != current_status:
            # Add new status to the job
            status_model.objects.create(job=self,
                                        status=status,
                                        message=message,
                                        details=details)
            return True
        return False


class JobStatus(models.Model):
    """A model that represents job status at certain time."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    # job = models.ForeignKey(Job, related_name='statuses')  # Must be implemented in subclasses
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
        return '{} <{}>'.format(self.job.unique_name, self.status)

    class Meta:
        verbose_name_plural = 'Job Statuses'
        ordering = ['created_at']
        abstract = True
