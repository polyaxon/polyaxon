# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.db import models

from libs.models import DiffModel
from projects.models import Project


class Repo(DiffModel):
    """A model that represents a repository containing code."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repos')
    project = models.OneToOneField(Project, related_name='repo')
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')


class RepoRevision(DiffModel):
    """A model that represents a repository containing code."""
    repo = models.ForeignKey(Repo, related_name='revisions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='revisions')
    commit = models.CharField(max_length=256)
    message = models.TextField(null=True, blank=True)
