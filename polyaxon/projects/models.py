import uuid

from django.conf import settings
from django.core.validators import validate_slug
from django.db import models

from libs.blacklist import validate_blacklist_name
from libs.models import DescribableModel, DiffModel
from plugins.models import NotebookJob, TensorboardJob


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
    tensorboard = models.OneToOneField(
        TensorboardJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    notebook = models.OneToOneField(
        NotebookJob,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    has_tensorboard = models.BooleanField(
        default=False,
        help_text='If project has a tensorboard.')
    has_notebook = models.BooleanField(
        default=False,
        help_text='If project has a notebook.')

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
