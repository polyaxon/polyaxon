import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from libs.blacklist import validate_blacklist_name
from libs.models import DescribableModel, DiffModel


class Project(DiffModel, DescribableModel):
    """A model that represents a set of experiments to solve a specific problem."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    name = models.CharField(
        max_length=256,
        validators=[validate_slug, validate_blacklist_name])
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
        unique_together = (('user', 'name'),)

    @property
    def unique_name(self):
        return '{}.{}'.format(self.user.username, self.name)

    @property
    def has_code(self):
        return hasattr(self, 'repo')

    @property
    def has_description(self):
        return bool(self.description)

    @property
    def tensorboard(self):
        if settings.DEPLOY_RUNNER:
            return self.tensorboard_jobs.last()
        return None

    @property
    def notebook(self):
        if settings.DEPLOY_RUNNER:
            return self.notebook_jobs.last()
        return None

    @property
    def has_tensorboard(self):
        tensorboard = self.tensorboard
        return tensorboard and tensorboard.is_running

    @property
    def has_notebook(self):
        notebook = self.notebook
        return notebook and notebook.is_running
