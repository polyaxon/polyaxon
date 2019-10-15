# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from schemas.exceptions import PolyaxonConfigurationError
from schemas.polyflow.ops import OpConfig
from schemas.specs import kinds
from schemas.specs.base import BaseSpecification


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

    _SPEC_KIND = kinds.OPERATION

    TEMPLATE = "template"
    I_TEMPLATE = "_template"

    SECTIONS = BaseSpecification.SECTIONS + (TEMPLATE, I_TEMPLATE)

    CONFIG = OpConfig

    def apply_context(self):
        raise PolyaxonConfigurationError(
            "This method is not allowed on this specification."
        )

    def apply_container_contexts(self, contexts=None):
        raise PolyaxonConfigurationError(
            "This method is not allowed on this specification."
        )

    def generate_run_data(self, override=None):
        values = [self.config._template.to_light_dict()]
        op_override = {}
        for field in [
            self.NAME,
            self.DESCRIPTION,
            self.TAGS,
            self.ENVIRONMENT,
            self.TERMINATION,
            self.INIT,
            self.MOUNTS,
            self.REPLICA_SPEC,
            self.PROFILE,
            self.NOCACHE
        ]:
            override_field = getattr(self.config, field)
            if override_field:
                op_override[field] = override_field
        if op_override:
            values.append(op_override)
        if override:
            values.append(override)
        return values
