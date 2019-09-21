# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy

from polyaxon_schemas.polyflow.ops import OpConfig
from polyaxon_schemas.polyflow.pipeline import PipelineConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseSpecification


class OperationSpecificationMixin(object):
    @property
    def dependencies(self):
        return self.config.dependencies

    @property
    def trigger(self):
        return self.config.trigger

    @property
    def conditions(self):
        return self.config.conditions

    @property
    def skip_on_upstream_skip(self):
        return self.config.skip_on_upstream_skip


class OperationSpecification(BaseSpecification, OperationSpecificationMixin):
    """The polyaxonfile specification for pipelines.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
    """

    _SPEC_KIND = kinds.PIPELINE

    CONFIG = OpConfig

    @property
    def backend(self):
        return self.config.backend

    def apply_context(self, context=None):
        self.config.process_dag()
        self.config.validate_dag()
        self.config.process_templates()
        return self
