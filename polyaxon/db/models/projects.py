import uuid

from django.conf import settings
from django.db import models

from db.models.utils import DescribableModel, DiffModel, NameableModel


class Project(DiffModel, NameableModel, DescribableModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        return '{}.{}'.format(self.user.username, self.name)

    @property
    def has_code(self):
        return hasattr(self, 'repo')

    @property
    def tensorboard(self):
        return self.tensorboard_jobs.last()

    @property
    def notebook(self):
        return self.notebook_jobs.last()

    @property
    def has_tensorboard(self):
        tensorboard = self.tensorboard
        return tensorboard and tensorboard.is_running

    @property
    def has_notebook(self):
        notebook = self.notebook
        return notebook and notebook.is_running
