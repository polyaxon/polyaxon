from django.contrib.postgres.fields import JSONField

from django.db import models

from db.models.utils import DiffModel


class CI(DiffModel):
    project = models.OneToOneField(
        'db.Project',
        related_name='ci',
        on_delete=models.CASCADE)
    config = JSONField(
        blank=True,
        null=True,
        help_text='The ci config schema.')
