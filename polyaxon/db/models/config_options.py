from picklefield import PickledObjectField

from django.db import models
from django.utils.functional import cached_property

from db.models.abstract.diff import DiffModel
from db.models.abstract.unique_name import UniqueNameMixin
from db.models.fields.encrypted_pickledfield import EncryptedPickledObjectField


class ConfigOption(DiffModel, UniqueNameMixin):
    owner = models.ForeignKey(
        'db.Owner',
        related_name='config_options',
        on_delete=models.CASCADE)
    key = models.CharField(max_length=256)
    secret = EncryptedPickledObjectField(null=True, blank=True)
    value = PickledObjectField(null=True, blank=True)

    class Meta:
        app_label = 'db'
        unique_together = (('owner', 'key'),)
        indexes = [
            models.Index(fields=['owner', 'key']),
            models.Index(fields=['key']),
        ]

    def __str__(self):
        return self.unique_name

    @cached_property
    def unique_name(self):
        return '{} <{}>'.format(self.owner, self.key) if self.owner else '{}'.format(self.key)

    @property
    def is_secret(self):
        return self.secret is not None

    @property
    def is_value(self):
        return self.value is not None
