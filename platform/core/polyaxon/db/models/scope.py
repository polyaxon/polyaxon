from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ScopeModel(models.Model):
    """
    A model that represents a scope: Cluster/Org/Team/Project/Experiment.
    """
    scope_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='+')
    scope_object_id = models.PositiveIntegerField()
    scope = GenericForeignKey('scope_content_type', 'scope_object_id')

    class Meta:
        abstract = True
