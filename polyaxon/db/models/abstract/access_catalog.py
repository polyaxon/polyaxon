from django.db import models
from django.utils.functional import cached_property

from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import RequiredNameableModel
from db.models.abstract.secret import SecretModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.unique_names import ACCESS_UNIQUE_NAME_FORMAT


class AccessCatalog(RequiredNameableModel,
                    DescribableModel,
                    SecretModel,
                    DiffModel,
                    UniqueNameMixin):
    owner = models.ForeignKey(
        'db.Owner',
        on_delete=models.CASCADE,
        related_name='+')

    class Meta:
        abstract = True

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        if self.owner:
            return ACCESS_UNIQUE_NAME_FORMAT.format(owner=self.owner, name=self.name)
        return '{}'.format(self.name)


class HostAccessCatalog(AccessCatalog):
    host = models.URLField(max_length=256)

    class Meta:
        abstract = True
