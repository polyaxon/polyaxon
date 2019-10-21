#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.exceptions import PolyaxonConfigurationError
from polyaxon.schemas.polyflow.ops import OpConfig
from polyaxon.schemas.specs import kinds
from polyaxon.schemas.specs.base import BaseSpecification


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

    @property
    def is_template_job(self):
        return self.check_kind_job(self.config._template.kind)

    @property
    def is_template_service(self):
        return self.check_kind_service(self.config._template.kind)

    @property
    def is_template_pipeline(self):
        return self.check_kind_pipeline(self.config._template.kind)

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
            self.NOCACHE,
        ]:
            override_field = getattr(self.config, field)
            if hasattr(override_field, "to_dict"):
                op_override[field] = override_field.to_dict()
            elif override_field:
                op_override[field] = override_field
        if op_override:
            values.append(op_override)
        if override:
            values.append(override)
        return values
