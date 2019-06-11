from django.core.validators import validate_slug
from django.db import models

from libs.blacklist import validate_blacklist_name


class NameableModel(models.Model):
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        validators=[validate_slug, validate_blacklist_name])

    class Meta:
        abstract = True


class RequiredNameableModel(models.Model):
    name = models.CharField(
        max_length=128,
        validators=[validate_slug, validate_blacklist_name])

    class Meta:
        abstract = True
