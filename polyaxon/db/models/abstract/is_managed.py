from django.db import models


class IsManagedModel(models.Model):
    is_managed = models.BooleanField(default=True,
                                     help_text='If this entity is managed by the platform.')

    class Meta:
        abstract = True
