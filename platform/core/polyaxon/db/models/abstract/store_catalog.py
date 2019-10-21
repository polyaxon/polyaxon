from django.db import models

from constants.store_types import StoreTypes
from db.models.abstract.access_catalog import AccessCatalog


class StoreCatalogModel(AccessCatalog):
    type = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        choices=StoreTypes.CHOICES)
    mount_path = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    host_path = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    volume_claim = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    bucket = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    read_only = models.NullBooleanField(default=False)

    class Meta(AccessCatalog.Meta):
        abstract = True
