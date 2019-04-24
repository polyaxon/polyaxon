from typing import List, Optional

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from libs.spec_validation import validate_persistence_config
from schemas import PersistenceConfig


class PersistenceModel(models.Model):
    persistence = JSONField(
        null=True,
        blank=True,
        help_text='The persistence definition.',
        validators=[validate_persistence_config])

    class Meta:
        abstract = True

    @cached_property
    def persistence_config(self) -> Optional['PersistenceConfig']:
        return PersistenceConfig.from_dict(self.persistence) if self.persistence else None

    @cached_property
    def persistence_data(self) -> Optional[List[str]]:
        return self.persistence_config.data if self.persistence_config else None

    @cached_property
    def persistence_outputs(self) -> Optional[List[str]]:
        return self.persistence_config.outputs if self.persistence_config else None

    @cached_property
    def persistence_logs(self) -> Optional[List[str]]:
        return None
