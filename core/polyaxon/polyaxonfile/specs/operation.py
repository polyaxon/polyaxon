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

from collections.abc import Mapping
from typing import Dict, Union

from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyaxonfile.specs.base import BaseSpecification
from polyaxon.polyflow import (
    V1CompiledOperation,
    V1Component,
    V1Operation,
    validate_run_patch,
)
from polyaxon.utils.list_utils import to_list


class OperationSpecification(BaseSpecification):
    """The polyaxonfile specification for operations."""

    _SPEC_KIND = kinds.OPERATION

    CONFIG = V1Operation

    @classmethod
    def compile_operation(
        cls, config: V1Operation, override: Dict = None
    ) -> V1CompiledOperation:
        if override:
            preset = OperationSpecification.read(override, is_preset=True)
            config = config.patch(preset, preset.patch_strategy)
        # Patch run
        component = config.component  # type: V1Component
        if config.run_patch:
            component.run = component.run.patch(
                validate_run_patch(config.run_patch, component.run.kind),
                strategy=config.patch_strategy,
            )
        patch_compiled = V1CompiledOperation(
            name=config.name,
            description=config.description,
            tags=config.tags,
            presets=config.presets,
            queue=config.queue,
            cache=config.cache,
            hooks=config.hooks,
            actions=config.actions,
            events=config.events,
            plugins=config.plugins,
            termination=config.termination,
            matrix=config.matrix,
            schedule=config.schedule,
            dependencies=config.dependencies,
            trigger=config.trigger,
            conditions=config.conditions,
            skip_on_upstream_skip=config.skip_on_upstream_skip,
        )

        values = [
            {cls.VERSION: config.version},
            component.to_dict(),
            {cls.KIND: kinds.COMPILED_OPERATION},
        ]
        compiled = V1CompiledOperation.read(values)  # type: V1CompiledOperation
        return compiled.patch(patch_compiled, strategy=config.patch_strategy)

    @classmethod
    def apply_preset(
        cls, config: V1CompiledOperation, preset: Union[Dict, str] = None
    ) -> V1CompiledOperation:
        if not preset:
            return config
        preset = OperationSpecification.read(
            preset, is_preset=True
        )  # type: V1Operation
        if preset.run_patch:
            config.run = config.run.patch(
                validate_run_patch(preset.run_patch, config.run.kind),
                strategy=preset.patch_strategy,
            )
        patch_compiled = V1CompiledOperation(
            name=preset.name,
            description=preset.description,
            tags=preset.tags,
            presets=preset.presets,
            queue=preset.queue,
            cache=preset.cache,
            hooks=preset.hooks,
            actions=preset.actions,
            events=preset.events,
            plugins=preset.plugins,
            termination=preset.termination,
            matrix=preset.matrix,
            schedule=preset.schedule,
            dependencies=preset.dependencies,
            trigger=preset.trigger,
            conditions=preset.conditions,
            skip_on_upstream_skip=preset.skip_on_upstream_skip,
        )
        return config.patch(patch_compiled, strategy=preset.patch_strategy)

    @classmethod
    def read(cls, values, is_preset: bool = False):
        if is_preset:
            if isinstance(values, cls.CONFIG):
                values.is_preset = True
                return values
            elif isinstance(values, Mapping):
                values[cls.IS_PRESET] = True
            else:
                values = to_list(values)
                values = [{cls.IS_PRESET: True}] + values

        return super().read(values)
