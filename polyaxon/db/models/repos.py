import os

from typing import Any, Tuple

from django.db import models

import conf

from constants.urls import API_V1
from db.models.utils import DiffModel


class RepoMixin(object):
    @property
    def user_path(self) -> str:
        return os.path.join(conf.get('REPOS_MOUNT_PATH'), self.project.user.username)

    @property
    def project_path(self) -> str:
        return os.path.join(self.user_path, self.project.name)

    @property
    def path(self) -> str:
        """We need to nest the git path inside the project path to make it easier
        to create docker images."""
        return os.path.join(self.project_path, self.project.name)

    @property
    def git(self) -> Any:
        from libs.repos import git

        return git.get_git_repo(repo_path=self.path)

    @property
    def last_commit(self) -> Tuple:
        """Returns a tuple (hash, and commit object)"""
        from libs.repos import git

        return git.get_last_commit(repo_path=self.path)

    @property
    def last_code_reference(self):
        """Returns the last code reference"""
        return self.references.last()

    def get_tmp_tar_path(self) -> str:
        return os.path.join(self.path, '{}_new.tar.gz'.format(self.project.name))

    @property
    def download_url(self) -> str:
        return '{}/{}/{}/repo/download'.format(API_V1,
                                               self.project.user.username,
                                               self.project.name)


class Repo(DiffModel, RepoMixin):
    """A model that represents a repository containing code."""
    project = models.OneToOneField(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='repo')
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')

    class Meta:
        app_label = 'db'

    def __str__(self) -> str:
        return '{} <repo>'.format(self.project)


class ExternalRepo(DiffModel, RepoMixin):
    """A model that represents an external repository containing code."""
    project = models.OneToOneField(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='external_repo')
    git_url = models.URLField()
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'git_url'),)

    def __str__(self):
        return '{} - {}'.format(self.project, self.name)

    @property
    def name(self):
        git_name = self.git_url.split('/')[-1]
        return git_name.split('.git')[0]

    @property
    def path(self):
        """We need to nest the git path inside the project path to make it easier
        to create docker images."""
        return os.path.join(self.project_path, self.name)

    @property
    def git_clone_url(self):
        if self.is_public:
            return self.git_url

        from libs.repos import git

        return git.external.get_private_clone_url(git_url=self.git_url)


class CodeReference(DiffModel):
    """A model that represents a reference to repo and code commit."""
    repo = models.ForeignKey(
        'db.Repo',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='references')
    external_repo = models.ForeignKey(
        'db.ExternalRepo',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='references')
    branch = models.CharField(
        max_length=124,
        default='master',
        blank=True,
        null=True)
    commit = models.CharField(
        max_length=40,
        blank=True,
        null=True)
    head = models.CharField(
        max_length=40,
        blank=True,
        null=True)
    is_dirty = models.BooleanField(default=False)
    git_url = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        app_label = 'db'

    def __str__(self) -> str:
        return '{} <{}>'.format(self.repo, self.commit)
