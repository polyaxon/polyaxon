from typing import List, Optional, Union

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property

from libs.spec_validation import validate_outputs_config
from schemas import OutputsConfig


class OutputsModel(models.Model):
    outputs = JSONField(
        null=True,
        blank=True,
        help_text='The persistence definition.',
        validators=[validate_outputs_config])
    outputs_refs = models.OneToOneField(
        'db.OutputsRefs',
        related_name='+',
        blank=True,
        null=True,
        editable=False,
        on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @cached_property
    def outputs_config(self) -> Optional['OutputsConfig']:
        return OutputsConfig.from_dict(self.outputs) if self.outputs else None

    @cached_property
    def outputs_jobs(self) -> Optional[List[Union[str, int]]]:
        return self.outputs_config.jobs if self.outputs_config else None

    @cached_property
    def outputs_experiments(self) -> Optional[List[Union[str, int]]]:
        return self.outputs_config.experiments if self.outputs_config else None

    @cached_property
    def outputs_refs_jobs(self):
        if not self.outputs_refs:
            return None

        specs = self.outputs_refs.get_jobs_outputs_spec()
        if not specs:
            return None

        # Return an ordered list
        refs = []
        for job in self.outputs_jobs:
            refs.append(specs[int(job)])

        return refs

    @cached_property
    def outputs_refs_experiments(self):
        if not self.outputs_refs:
            return None

        specs = self.outputs_refs.get_experiments_outputs_spec()
        if not specs:
            return None

        # Return an ordered list
        refs = []
        for experiment in self.outputs_experiments:
            refs.append(specs[int(experiment)])

        return refs
