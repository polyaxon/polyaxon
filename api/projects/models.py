# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.db import models

from libs.models import DiffModel


class Project(DiffModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects')
    name = models.CharField(
        max_length=256,
        help_text='Name of the project.')
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Description of the project.')
    is_public = models.BooleanField(default=True, help_text='If project is public or private.')

    def __str__(self):
        return self.name


class Polyaxonfile(DiffModel):
    """A model that saves Polyaonfiles."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='polyaxonfiles')
    content = models.TextField(help_text='The yaml content of the polyaxonfile.')
    project = models.ForeignKey(
        Project,
        related_name='polyaxonfiles',
        help_text='The project this polyaxonfile belongs to.')
