#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import copy

from typing import Dict, List, Union

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile.specs.libs.parser import Parser
from polyaxon.polyflow import V1CompiledOperation, V1MatrixKind, V1Operation, V1Param
from polyaxon.utils.formatting import Printer


def get_op_from_schedule(
    content: str,
    compiled_operation: V1CompiledOperation,
) -> V1Operation:
    op_spec = V1Operation.read(content)
    op_spec.conditions = None
    op_spec.schedule = None
    op_spec.events = None
    op_spec.dependencies = None
    op_spec.trigger = None
    op_spec.skip_on_upstream_skip = None
    op_spec.cache = compiled_operation.cache
    op_spec.queue = compiled_operation.queue
    op_spec.component.inputs = compiled_operation.inputs
    op_spec.component.outputs = compiled_operation.outputs
    op_spec.component.contexts = compiled_operation.contexts
    return op_spec


def get_ops_from_suggestions(
    content: str,
    compiled_operation: V1CompiledOperation,
    suggestions: List[Dict],
) -> List[V1Operation]:
    def has_param(k: str):
        if not compiled_operation.matrix:
            return None
        return not compiled_operation.matrix.has_param(k)

    op_content = V1Operation.read(content)
    for suggestion in suggestions:
        params = {
            k: V1Param(value=Parser.parse_expression(v, {}), context_only=has_param(k))
            for (k, v) in suggestion.items()
        }
        op_spec = copy.deepcopy(op_content)
        op_spec.matrix = None
        op_spec.conditions = None
        op_spec.schedule = None
        op_spec.events = None
        op_spec.dependencies = None
        op_spec.trigger = None
        op_spec.skip_on_upstream_skip = None
        op_spec.cache = compiled_operation.cache
        op_spec.queue = compiled_operation.queue
        op_spec.params = params
        op_spec.component.inputs = compiled_operation.inputs
        op_spec.component.outputs = compiled_operation.outputs
        op_spec.component.contexts = compiled_operation.contexts
        yield op_spec


def get_eager_matrix_operations(
    content: str,
    compiled_operation: V1CompiledOperation,
    is_cli: bool = False,
) -> List[V1Operation]:
    is_supported_in_eager_mode(compiled_operation)

    try:
        import numpy as np
    except ImportError as e:
        if is_cli:
            Printer.print_error(
                "numpy is required for the eager mode, "
                "please run 'pip install polyaxon[numpy]'",
                sys_exit=True,
            )
        raise e

    from polyaxon.polytune.search_managers.grid_search.manager import GridSearchManager
    from polyaxon.polytune.search_managers.mapping.manager import MappingManager
    from polyaxon.polytune.search_managers.random_search.manager import (
        RandomSearchManager,
    )

    if compiled_operation.has_random_search_matrix:
        suggestions = RandomSearchManager(compiled_operation.matrix).get_suggestions()
    elif compiled_operation.has_grid_search_matrix:
        suggestions = GridSearchManager(compiled_operation.matrix).get_suggestions()
    elif compiled_operation.has_mapping_matrix:
        suggestions = MappingManager(compiled_operation.matrix).get_suggestions()
    else:
        raise PolyaxonSchemaError(
            "Received a bad configuration, eager mode not supported, "
            "I should not be here!"
        )
    if is_cli:
        Printer.print_header("Creating {} operations".format(len(suggestions)))
    return get_ops_from_suggestions(
        content=content, compiled_operation=compiled_operation, suggestions=suggestions
    )


def is_supported_in_eager_mode(spec: Union[V1Operation, V1CompiledOperation]):
    if not spec.matrix:
        if spec.component and spec.component.run:
            raise PolyaxonSchemaError(
                "This operation with runtime `{}` "
                "is not supported in eager mode".format(spec.component.run.kind)
            )
        else:
            raise PolyaxonSchemaError(
                "Received a bad configuration, eager mode not supported"
            )

    if spec.get_matrix_kind() not in V1MatrixKind.eager_values:
        raise PolyaxonSchemaError(
            "This operation is defining a matrix kind `{}` "
            "which is not supported in eager mode".format(spec.get_matrix_kind())
        )
