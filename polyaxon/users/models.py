from django.conf import settings
from django.db import models

from libs.models import DiffModel


class Profile(DiffModel):
    """A model that represents a user profile"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile')
    is_managed = models.BooleanField(
        default=False,
        help_text=(
            'Whether this user is managed. This disallows the user '
            'from modifying the account properties (username, password, etc).'))
