import uuid as uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract.deleted import DeletedModel
from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import RequiredNameableModel
from db.models.abstract.owner import OwnerMixin
from db.models.abstract.readme import ReadmeModel
from db.models.abstract.secret import SecretModel
from db.models.abstract.tag import TagModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.unique_names import CATALOG_UNIQUE_NAME_FORMAT


class Catalog(RequiredNameableModel,
              DescribableModel,
              DiffModel,
              ReadmeModel,
              TagModel,
              DeletedModel,
              OwnerMixin,
              UniqueNameMixin):
    owner = models.ForeignKey(
        'db.Owner',
        on_delete=models.CASCADE,
        related_name='+')
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        if self.owner:
            return CATALOG_UNIQUE_NAME_FORMAT.format(owner=self.owner, name=self.name)
        return '{}'.format(self.name)


class K8SResourceCatalog(Catalog):
    k8s_ref = models.CharField(max_length=256)
    keys = ArrayField(models.CharField(max_length=256), default=list, blank=True)

    class Meta:
        abstract = True


class AccessCatalog(Catalog, SecretModel):

    class Meta:
        abstract = True


class HostAccessCatalog(AccessCatalog):
    host = models.URLField(max_length=256)

    class Meta:
        abstract = True
