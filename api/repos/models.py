# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete

from libs.models import DiffModel
from projects.models import Project
from repos.signals import new_repo, repo_deleted


class Repo(DiffModel):
    """A model that represents a repository containing code."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repos')
    project = models.OneToOneField(Project, related_name='repo')
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')

    @property
    def path(self):
        return os.path.join(settings.REPOS_ROOT, self.user.username, self.project.name)

    def get_tmp_tar_path(self):
        return os.path.join(self.path, '{}_new.tar.gz'.format(self.project.name))


post_save.connect(new_repo, sender=Repo, dispatch_uid="repo_saved")
post_delete.connect(repo_deleted, sender=Repo, dispatch_uid="repo_deleted")


class RepoRevision(DiffModel):
    """A model that represents a repository containing code."""
    repo = models.ForeignKey(Repo, related_name='revisions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='revisions')
    commit = models.CharField(max_length=256)
    message = models.TextField(null=True, blank=True)
