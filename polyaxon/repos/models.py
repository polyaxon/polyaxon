import os

from django.conf import settings
from django.db import models

from libs.models import DiffModel
from models.projects import Project
from repos import git


class RepoMixin(object):
    @property
    def user_path(self):
        return os.path.join(settings.REPOS_ROOT, self.project.user.username)

    @property
    def project_path(self):
        return os.path.join(self.user_path, self.project.name)

    @property
    def path(self):
        """We need to nest the git path inside the project path to make it easier
        to create docker images."""
        return os.path.join(self.project_path, self.project.name)

    @property
    def git(self):
        return git.get_git_repo(repo_path=self.path)

    @property
    def last_commit(self):
        """Returns a tuple (hash, and commit object)"""
        return git.get_last_commit(repo_path=self.path)

    def get_tmp_tar_path(self):
        return os.path.join(self.path, '{}_new.tar.gz'.format(self.project.name))


class Repo(DiffModel, RepoMixin):
    """A model that represents a repository containing code."""
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='repo')
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')

    def __str__(self):
        return '{} <repo>'.format(self.project)


class ExternalRepo(DiffModel, RepoMixin):
    """A model that represents an external repository containing code."""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='external_repos')
    git_url = models.URLField()
    is_public = models.BooleanField(default=True, help_text='If repo is public or private.')

    class Meta:
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


class CodeReference(DiffModel):
    """A model that represents a reference to repo and code commit."""
    repo = models.ForeignKey(
        Repo,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='references')
    external_repo = models.ForeignKey(
        ExternalRepo,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='references')
    commit = models.CharField(
        max_length=40,
        blank=True,
        null=True)

    def __str__(self):
        return '{} <{}>'.format(self.repo, self.commit)
