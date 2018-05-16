from django.conf import settings
from django.db import models
from django.utils import timezone

from libs.models import DiffModel
from sso.providers.constants import PROVIDERS


class SSOProvider(DiffModel):
    name = models.CharField(max_length=54,
                            choices=PROVIDERS.CHOICES)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SSOIdentity(DiffModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='identities'
    )
    auth_provider = models.ForeignKey(SSOProvider, models.CASCADE)
    last_verified = models.DateTimeField(default=timezone.now)
    last_synced = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('auth_provider', 'user'),)

    def __str__(self):
        return '{} - {}'.format(self.user, self.auth_provider)

    def is_valid(self):
        if not self.auth_provider.is_enabled:
            return False
        if not self.last_verified:
            return False
        verification_schedule = PROVIDERS.get_verification_schedule(self.auth_provider.name)
        if self.last_verified < timezone.now() - verification_schedule:
            return False
        return True
