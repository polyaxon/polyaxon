from django.db import models


class BackendModel(models.Model):
    backend = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        help_text='The default backend use for running this entity.')

    class Meta:
        abstract = True
