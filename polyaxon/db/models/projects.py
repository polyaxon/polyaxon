import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import validate_slug
from django.db import models
from django.utils.functional import cached_property

import ownership
from db.models.abstract_jobs import TensorboardJobMixin
from db.models.unique_names import PROJECT_UNIQUE_NAME_FORMAT
from db.models.utils import DescribableModel, DiffModel, ReadmeModel, TagModel
from libs.blacklist import validate_blacklist_name


class Project(DiffModel, DescribableModel, ReadmeModel, TagModel, TensorboardJobMixin):
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
    owner_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE)
    owner_object_id = models.PositiveIntegerField()
    owner = GenericForeignKey('owner_content_type', 'owner_object_id')
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

    @cached_property
    def owner_details(self):
        return ownership.get_owner(self)

    @property
    def has_owner(self):
        """Quick test to check the instance has an owner."""
        return ownership.has_owner(self)
