# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.db import models

from libs.models import DiffModel


class Project(DiffModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    name = models.CharField(max_length=256, help_text='Name of the project.')
    description = models.TextField(blank=True, null=True, help_text='Description of the project.')
    is_public = models.BooleanField(default=True, help_text='If project is public or private.')

    def __str__(self):
        return self.name

    @property
    def experiments(self):
        return None

    @property
    def polyaxonfiles(self):
        return self.polyaxonfile.all()


class PolyaxonFile(DiffModel):
    """A model that saves Polyaonfiles."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    content = models.TextField(help_text='The yaml content of the polyaxonfile.')
    project = models.ForeignKey(Project, related_name='polyaxonfile',
                                help_text='The project this polyaxonfile belongs to.')

    @property
    def experiments(self):
        return self.experiment.all()
