from hestia.decorators import ignore_raw, ignore_updates
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver

import auditor
import ownership

from event_manager.events.user import USER_REGISTERED, USER_UPDATED


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_auth_token")
@ignore_raw
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        auditor.record(event_type=USER_REGISTERED, instance=instance)
    else:
        auditor.record(event_type=USER_UPDATED, instance=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_user_owner")
@ignore_updates
@ignore_raw
def create_user_owner(sender, instance=None, created=False, **kwargs):
    ownership.create_owner(
        name=instance.username,
        owner_obj=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL, dispatch_uid="delete_user_owner")
@ignore_raw
def delete_user_owner(sender, instance=None, created=False, **kwargs):
    ownership.delete_owner(name=instance.username)


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])
