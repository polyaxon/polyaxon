#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from typing import Dict

from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyaxonfile.specs.base import BaseSpecification
from polyaxon.polyflow import V1CompiledOperation, V1Operation


class OperationSpecification(BaseSpecification):
    """The polyaxonfile specification for operations."""

    _SPEC_KIND = kinds.OPERATION

    CONFIG = V1Operation

    @classmethod
    def compile_operation(
        cls, config: V1Operation, override: Dict = None, override_post: bool = True
    ) -> V1CompiledOperation:
        return V1CompiledOperation.read(
            cls.generate_run_data(config, override, override_post)
        )

    @classmethod
    def generate_run_data(cls, config: V1Operation, override=None, override_post=True):
        op_config = config.to_light_dict()
        name = None
        if config.component:
            name = config.component.get_name()
        component_config = op_config.pop("component", {})
        if name:
            component_config["name"] = name
        values = [
            {"version": config.version},
            component_config,
            {"kind": kinds.COMPILED_OPERATION},
        ]
        op_override = {}
        for field in [
            cls.NAME,
            cls.DESCRIPTION,
            cls.TAGS,
            cls.PROFILE,
            cls.QUEUE,
            cls.CACHE,
            cls.PLUGINS,
            cls.TERMINATION,
            cls.MATRIX,
            cls.SCHEDULE,
            cls.DEPENDENCIES,
            cls.TRIGGER,
            cls.CONDITIONS,
            cls.SKIP_ON_UPSTREAM_SKIP,
        ]:
            override_field = op_config.get(field)
            if override_field:
                op_override[field] = override_field
        # Patch run
        run_patch = op_config.get(cls.RUN_PATCH)
        if run_patch:
            op_override[cls.RUN] = run_patch
        if override_post:
            if op_override:
                values.append(op_override)
            if override:
                values.append(override)
        else:
            if override:
                values.append(override)
            if op_override:
                values.append(op_override)
        return values
