from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models


class ActivityLog(models.Model):
    """The ActivityLog model represents one recorded event."""
    ref = models.UUIDField(editable=False)
    event_type = models.CharField(max_length=128)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True,
        help_text='The user who triggered this activity, if null we assume a user `system`.')
    context = JSONField(help_text='Extra context information.')
    created_at = models.DateTimeField()

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'db'
        verbose_name = 'activity log'
        verbose_name_plural = 'activities logs'

    def __str__(self) -> str:
        return '{} - {}'.format(self.event_type, self.created_at)
