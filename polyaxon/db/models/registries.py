from django.db import models
from django.utils.functional import cached_property

from db.models.abstract.describable import DescribableModel
from db.models.abstract.diff import DiffModel
from db.models.abstract.nameable import RequiredNameableModel
from db.models.abstract.secret import SecretModel
from db.models.abstract.unique_name import UniqueNameMixin


class Registry(RequiredNameableModel, DescribableModel, SecretModel, DiffModel, UniqueNameMixin):
    owner = models.ForeignKey(
        'db.Owner',
        on_delete=models.CASCADE,
        related_name='+')
    host = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None)

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'name'),)

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self) -> str:
        return '{} <{}>'.format(self.owner, self.name) if self.owner else '{}'.format(self.name)
