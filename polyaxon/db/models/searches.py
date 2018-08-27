from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from db.models.utils import DiffModel, NameableModel


class Search(DiffModel, NameableModel):
    """A saved search query."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='searches')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    query = models.TextField()
    is_default = models.BooleanField(default=False)

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'), )
