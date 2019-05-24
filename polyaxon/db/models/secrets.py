from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.functional import cached_property

from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import NameableModel
from db.models.abstract.unique_name import UniqueNameMixin


class K8SSecret(NameableModel, DiffModel, DescribableModel, UniqueNameMixin):
    """A model to represent a catalog of k8s secrets.

    Since k8s secrets can hold several entries,
    often time the user only requires mounting some of these keys.

    N.B. If no keys are specified, the whole secret will be mounted to the requiting jobs.
    """
    owner = models.ForeignKey(
        'db.Owner',
        on_delete=models.CASCADE,
        related_name='+')
    secret_ref = models.CharField(max_length=256)
    keys = ArrayField(models.CharField(max_length=256), default=list, blank=True)

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        return '{} <{}>'.format(self.owner, self.name) if self.owner else '{}'.format(self.name)
