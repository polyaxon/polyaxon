from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from db.models.utils import DiffModel


class CI(DiffModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    project = models.OneToOneField(
        'db.Project',
        related_name='ci',
        on_delete=models.CASCADE)
    config = JSONField(
        blank=True,
        null=True,
        help_text='The ci config schema.')
    code_reference = models.ForeignKey(
        'db.CodeReference',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+',
        help_text="The ci's last code ref used.")
