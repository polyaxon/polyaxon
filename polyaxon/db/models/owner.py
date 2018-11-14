from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import validate_unicode_slug
from django.db import models
from django.utils.functional import cached_property

from db.models.utils import DiffModel


class Owner(DiffModel):
    """A model that represents a project owner."""
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='+')
    object_id = models.PositiveIntegerField()
    owner = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_unicode_slug]
    )

    class Meta:
        app_label = 'db'
        unique_together = (('content_type', 'object_id'),)

    @cached_property
    def owner_type(self):
        return self.content_type.model
