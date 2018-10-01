from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from constants import content_types
from db.models.utils import DiffModel, NameableModel


class Search(DiffModel, NameableModel):
    """A saved search query."""
    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='searches')
    content_type = models.CharField(
        choices=content_types.CHOICES,
        max_length=24,
        blank=True,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    query = JSONField()
    meta = JSONField(
        null=True,
        blank=True,
        default=dict
    )

    class Meta:
        app_label = 'db'
        unique_together = (('project', 'name'), )
