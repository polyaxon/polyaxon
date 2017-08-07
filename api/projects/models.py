# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.db import models

from core.models import Experiment
from libs.models import DiffModel


class Project(DiffModel):
    """The `Project` model represents a set of experiments to solve a specific problem."""
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    experiments = models.ManyToManyField(Experiment)

    def __str__(self):
        return self.name
