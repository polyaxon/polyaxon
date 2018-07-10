from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from db.models.utils import DiffModel


class Bookmark(DiffModel):
    """The Bookmark model represents an instance of object that user bookmarked."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+')
    enabled = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'db'
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmarks'

    def __str__(self):
        return '{} - <{}-{}>'.format(self.user, self.content_type, self.created_at)
