from django.contrib.postgres.fields import JSONField
from django.db import models


class DataReference(models.Model):
    data_refs = JSONField(
        null=True,
        blank=True,
        help_text='The data hashes used.')

    class Meta:
        abstract = True
