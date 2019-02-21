import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import TensorboardJobMixin
from db.models.unique_names import PROJECT_UNIQUE_NAME_FORMAT
from db.models.utils import (
    DeletedModel,
    DescribableModel,
    DiffModel,
    PersistenceModel,
    ReadmeModel,
    SubPathModel,
    TagModel
)
from libs.blacklist import validate_blacklist_name
from libs.paths.projects import get_project_subpath


class Project(DiffModel,
              DescribableModel,
              ReadmeModel,
              TagModel,
              DeletedModel,
              PersistenceModel,
              SubPathModel,
              TensorboardJobMixin):
    """A model that represents a set of experiments to solve a specific problem."""
    CACHED_PROPERTIES = ['notebook', 'has_notebook', 'tensorboard', 'has_tensorboard']

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    name = models.CharField(
        max_length=128,
        validators=[validate_slug, validate_blacklist_name])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects')
    owner = models.ForeignKey(
        'db.Owner',
        on_delete=models.CASCADE,
        related_name='projects')
    is_public = models.BooleanField(
        default=True,
        help_text='If project is public or private.')

    def __str__(self) -> str:
        return self.unique_name

    class Meta:
        app_label = 'db'
        unique_together = (('user', 'name'),)

    @property
    def unique_name(self) -> str:
        return PROJECT_UNIQUE_NAME_FORMAT.format(
            user=self.user.username,
            project=self.name)

    @property
    def subpath(self) -> str:
        return get_project_subpath(project_name=self.unique_name)

    @property
    def has_code(self) -> bool:
        return self.has_repo or self.has_external_repo

    @property
    def has_repo(self):
        return hasattr(self, 'repo')

    @property
    def has_external_repo(self):
        return hasattr(self, 'external_repo')

    @property
    def has_ci(self):
        return hasattr(self, 'ci')

    @cached_property
    def notebook(self):
        return self.notebook_jobs.last()

    @cached_property
    def has_notebook(self) -> bool:
        notebook = self.notebook
        return notebook and notebook.is_stoppable

    @cached_property
    def tensorboard(self):
        return self.tensorboard_jobs.filter(experiment=None, experiment_group=None).last()

    @property
    def all_experiments(self):
        """
        Similar to experiments,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.experiments import Experiment

        return Experiment.all.filter(project=self)

    @property
    def all_experiment_groups(self):
        """
        Similar to experiment_groups,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.experiment_groups import ExperimentGroup

        return ExperimentGroup.all.filter(project=self)

    @property
    def all_jobs(self):
        """
        Similar to jobs,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.jobs import Job

        return Job.all.filter(project=self)

    @property
    def all_build_jobs(self):
        """
        Similar to build_jobs,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.build_jobs import BuildJob

        return BuildJob.all.filter(project=self)

    @property
    def all_notebook_jobs(self):
        """
        Similar to notebook_jobs,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.notebooks import NotebookJob

        return NotebookJob.all.filter(project=self)

    @property
    def all_tensorboard_jobs(self):
        """
        Similar to tensorboard_jobs,
        but uses the default manager to return archived experiments as well.
        """
        from db.models.tensorboards import TensorboardJob

        return TensorboardJob.all.filter(project=self)

    @property
    def has_owner(self) -> bool:
        """Quick test to check the instance has an owner."""
        return bool(self.owner_id)

    def archive(self) -> bool:
        if not super().archive():
            return False
        self.experiment_groups.update(deleted=True)
        self.experiments.update(deleted=True)
        self.jobs.update(deleted=True)
        self.build_jobs.update(deleted=True)
        self.notebook_jobs.update(deleted=True)
        self.tensorboard_jobs.update(deleted=True)
        return True

    def restore(self) -> bool:
        if not super().restore():
            return False
        self.all_experiment_groups.update(deleted=False)
        self.all_experiments.update(deleted=False)
        self.all_jobs.update(deleted=False)
        self.all_build_jobs.update(deleted=False)
        self.all_notebook_jobs.update(deleted=False)
        self.all_tensorboard_jobs.update(deleted=False)
        return True
