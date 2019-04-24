from django.db import models

from constants.backends import NATIVE_BACKEND


class BackendModel(models.Model):
    backend = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        default=NATIVE_BACKEND,
        help_text='The default backend use for running this entity.')

    class Meta:
        abstract = True
