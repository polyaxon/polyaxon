# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from libs.blacklist import validate_blacklist_name
from libs.models import DiffModel, DescribableModel
from projects.models import Project


class Dataset(DiffModel, DescribableModel):
    """A model that represents a dataset."""
    name = models.CharField(max_length=256, validators=[validate_slug, validate_blacklist_name])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='datasets')
    version = models.IntegerField(default=1)
    is_public = models.BooleanField(default=True, help_text='If dataset is public or private.')

    @property
    def user_path(self):
        return os.path.join(settings.DATA_ROOT, self.user.username)

    @property
    def path(self):
        return os.path.join(self.user_path, self.name, str(self.version))

    def get_tmp_tar_path(self):
        return os.path.join(self.path, '{}_new.tar.gz'.format(self.name))

    @property
    def path(self):
        """We need to nest the git path inside the project path to make it easier
        to create docker images."""
        return os.path.join(self.project_path, self.name)
