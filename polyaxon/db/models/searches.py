from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from constants import content_types
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import NameableModel


class Search(DiffModel, NameableModel):
    """A saved search query."""
    search_content_types = (
        (content_types.PROJECT, content_types.PROJECT),
        (content_types.EXPERIMENT_GROUP, content_types.EXPERIMENT_GROUP),
        (content_types.EXPERIMENT, content_types.EXPERIMENT),
        (content_types.JOB, content_types.JOB),
        (content_types.BUILD_JOB, content_types.BUILD_JOB),
    )

    project = models.ForeignKey(
        'db.Project',
        on_delete=models.CASCADE,
        related_name='searches')
    content_type = models.CharField(
        choices=search_content_types,
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
        unique_together = (('user', 'project', 'name'), )
