from django.db import models
from django.utils.functional import cached_property

from constants.store_types import StoreTypes
from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import RequiredNameableModel
from db.models.abstract.secret import SecretModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.unique_names import STORE_UNIQUE_NAME_FORMAT


class StoreCatalogModel(RequiredNameableModel,
                        DescribableModel,
                        SecretModel,
                        DiffModel,
                        UniqueNameMixin):
    owner = models.ForeignKey(
        'db.Owner',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+')
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        if self.owner:
            return STORE_UNIQUE_NAME_FORMAT.format(owner=self.owner, name=self.name)
        return '{}'.format(self.name)
