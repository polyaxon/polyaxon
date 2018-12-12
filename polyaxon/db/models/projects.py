import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract_jobs import TensorboardJobMixin
from db.models.unique_names import PROJECT_UNIQUE_NAME_FORMAT
from db.models.utils import DescribableModel, DiffModel, ReadmeModel, TagModel, DeletedModel
from libs.blacklist import validate_blacklist_name


class Project(DiffModel,
              DescribableModel,
              ReadmeModel,
              TagModel,
              DeletedModel,
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

    def __str__(self):
        return self.unique_name

    class Meta:
        app_label = 'db'
        unique_together = (('user', 'name'),)

    @property
    def unique_name(self):
        return PROJECT_UNIQUE_NAME_FORMAT.format(
            user=self.user.username,
            project=self.name)

    @property
    def has_code(self):
        return hasattr(self, 'repo')

    @cached_property
    def notebook(self):
        return self.notebook_jobs.last()

    @cached_property
    def has_notebook(self):
        notebook = self.notebook
        return notebook and notebook.is_running

    @cached_property
    def tensorboard(self):
        return self.tensorboard_jobs.filter(experiment=None, experiment_group=None).last()

    @cached_property
    def has_tensorboard(self):
        tensorboard = self.tensorboard
        return tensorboard and tensorboard.is_running

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
    def has_owner(self):
        """Quick test to check the instance has an owner."""
        return bool(self.owner_id)

    def archive(self):
        super().archive()
        self.experiment_groups.update(deleted=True)
        self.experiments.update(deleted=True)
        self.jobs.update(deleted=True)
        self.build_jobs.update(deleted=True)
        self.notebook_jobs.update(deleted=True)
        self.tensorboard_jobs.update(deleted=True)
