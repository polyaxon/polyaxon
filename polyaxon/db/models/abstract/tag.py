from django.contrib.postgres.fields import ArrayField
from django.db import models


class TagModel(models.Model):
    tags = ArrayField(
        base_field=models.CharField(max_length=64),
        blank=True,
        null=True,
        help_text='The parameters used for this experiment.')

    class Meta:
        abstract = True
