# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon_schemas.polyflow.pipeline import PipelineConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseSpecification


class PipelineSpecification(BaseSpecification):
    """The polyaxonfile specification for pipelines.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
    """

    _SPEC_KIND = kinds.PIPELINE

    CONFIG = PipelineConfig

    @property
    def backend(self):
        return self.raw_config.backend

    def _get_config(self, data):
        config = self.CONFIG.from_dict(copy.deepcopy(data))
        return config

    def apply_context(self, context=None):
        self._config_data.process_dag()
        self._config_data.validate_dag()
        self._config_data.process_templates()
        self._config = self._config_data
        return self
