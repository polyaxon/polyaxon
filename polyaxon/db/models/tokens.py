from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from db.models.utils import DiffModel


def generate_token():
    return uuid4().hex + uuid4().hex


class Token(DiffModel):
    """A model that represents a token that could be used in behalf of any owner."""

    user = models.ForeignKey(
        'db.User',
        on_delete=models.CASCADE,
        related_name='tokens')
    key = models.CharField(
        max_length=64,
        unique=True,
        default=generate_token,
    )
    refresh_key = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        default=generate_token,
    )
    scopes = ArrayField(models.CharField(max_length=20), default=list, blank=True)
    started_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'db'

    @property
    def is_expired(self):
        return self.started_at + timedelta(days=settings.TOKEN_TTL) <= timezone.now()

    def has_scope(self, scope):
        return scope in self.scopes  # pylint:disable=unsupported-membership-test

    def refresh(self, started_at=None):
        self.update(
            key=generate_token(),
            refresh_key=generate_token(),
            started_at=started_at or timezone.now(),
        )
