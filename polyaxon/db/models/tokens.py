from datetime import timedelta
from uuid import uuid4

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

import conf

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

    def __str__(self) -> str:
        return 'Token <{}>'.format(self.user)

    @property
    def is_expired(self) -> bool:
        return self.started_at + timedelta(days=conf.get('TTL_TOKEN')) <= timezone.now()

    def has_scope(self, scope) -> bool:
        return scope in self.scopes  # pylint:disable=unsupported-membership-test

    def refresh(self, started_at=None) -> None:
        self.key = generate_token()
        self.refresh_key = generate_token()
        self.started_at = started_at or timezone.now()
        self.save(update_fields=['key', 'refresh_key', 'started_at'])
