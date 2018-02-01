# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from spawner.utils.constants import JobLifeCycle


class JobResources(models.Model):
    """A model that represents job resources."""
    cpu = JSONField(null=True, blank=True)
    memory = JSONField(null=True, blank=True)
    gpu = JSONField(null=True, blank=True)

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
