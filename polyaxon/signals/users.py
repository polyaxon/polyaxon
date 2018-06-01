from rest_framework.authtoken.models import Token

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

import auditor

from event_manager.events.user import USER_REGISTERED, USER_UPDATED
from libs.decorators import ignore_raw


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@ignore_raw
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        auditor.record(event_type=USER_REGISTERED, instance=instance)
    else:
        auditor.record(event_type=USER_UPDATED, instance=instance)


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])
