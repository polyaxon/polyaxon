# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from rest_framework.authtoken.models import Token

from libs.decorators import ignore_raw


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@ignore_raw
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])
