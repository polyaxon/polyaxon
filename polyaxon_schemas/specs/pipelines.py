# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from hestia.cached_property import cached_property

from polyaxon_schemas.polyflow.pipeline import PipelineConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseSpecification


class PipelineSpecification(BaseSpecification):
    """The polyaxonfile specification for pipelines.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = kinds.PIPELINE

    TEMPLATES = 'templates'
    OPS = 'ops'
    SCHEDULE = 'schedule'
    CONCURRENCY = 'concurrency'

    SECTIONS = BaseSpecification.SECTIONS + (TEMPLATES, OPS, SCHEDULE, CONCURRENCY)

    OP_PARSING_SECTIONS = BaseSpecification.OP_PARSING_SECTIONS + (
        TEMPLATES, OPS, SCHEDULE, CONCURRENCY)

    HEADER_SECTIONS = BaseSpecification.HEADER_SECTIONS + (BaseSpecification.BACKEND,)

    POSSIBLE_SECTIONS = BaseSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.BACKEND, BaseSpecification.ENVIRONMENT,
        TEMPLATES, OPS, SCHEDULE, CONCURRENCY
    )

    CONFIG = PipelineConfig

    @cached_property
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
