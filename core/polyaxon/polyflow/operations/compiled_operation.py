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
from typing import Dict, List

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyflow.io import V1IO, IOSchema
from polyaxon.polyflow.operations.base import BaseOp, BaseOpSchema
from polyaxon.polyflow.params import ParamSpec, ops_params
from polyaxon.polyflow.run import RunMixin, RunSchema


class CompiledOperationSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("compiled_operation"))
    inputs = fields.List(fields.Nested(IOSchema), allow_none=True)
    outputs = fields.List(fields.Nested(IOSchema), allow_none=True)
    contexts = fields.List(fields.Nested(IOSchema), allow_none=True)
    run = fields.Nested(RunSchema, required=True)

    @staticmethod
    def schema_config():
        return V1CompiledOperation


class V1CompiledOperation(BaseOp, RunMixin, polyaxon_sdk.V1CompiledOperation):
    SCHEMA = CompiledOperationSchema
    IDENTIFIER = "compiled_operation"
    REDUCED_ATTRIBUTES = BaseOp.REDUCED_ATTRIBUTES + [
        "inputs",
        "outputs",
        "contexts",
        "run",
    ]

    def get_run_kind(self):
        return self.run.kind if self.run else None

    def validate_params(
        self,
        params: Dict = None,
        context: Dict = None,
        is_template: bool = True,
        check_all_refs: bool = False,
        parse_values: bool = False,
        parse_joins: bool = True,
    ) -> List[ParamSpec]:
        return ops_params.validate_params(
            inputs=self.inputs,
            outputs=self.outputs,
            contexts=self.contexts,
            params=params,
            matrix=self.matrix,
            joins=self.joins if parse_joins else None,
            context=context,
            is_template=is_template,
            check_all_refs=check_all_refs,
            parse_values=parse_values,
        )

    def apply_params(self, params=None, context=None):
        context = context or {}
        validated_params = self.validate_params(
            params=params,
            context=context,
            is_template=False,
            check_all_refs=True,
            parse_values=True,
        )
        if not validated_params:
            return

        param_specs = {}
        for param in validated_params:
            param_specs[param.name] = param

        processed_params = set([])

        def set_io(io):
            if not io:
                return
            for i in io:
                if i.name in param_specs:
                    processed_params.add(i.name)
                    i.is_optional = True
                    if param_specs[i.name].param.is_literal:
                        current_param = param_specs[i.name].param
                        value = current_param.value
                        if hasattr(value, "to_param"):
                            value = value.to_param()
                        i.value = value
                        if current_param.connection:
                            i.connection = current_param.connection
                        if current_param.to_init:
                            i.to_init = current_param.to_init
                        if current_param.to_env:
                            i.to_env = current_param.to_env

        def set_contexts() -> List[V1IO]:
            context_params = [p for p in param_specs if p not in processed_params]
            contexts = []
            for p in context_params:
                current_param = param_specs[p].param
                contexts.append(
                    V1IO(
                        name=p,
                        value=current_param.value,
                        is_optional=True,
                        connection=current_param.connection,
                        to_init=current_param.to_init,
                        to_env=current_param.to_env,
                    )
                )

            return contexts

        set_io(self.inputs)
        set_io(self.outputs)
        self.contexts = set_contexts()

    def get_env_io(self) -> List[List]:
        def get_env_io(io: List[V1IO]) -> List[List]:
            return [[i.to_env, i.value] for i in io if i.to_env]

        return (
            get_env_io(self.inputs or [])
            + get_env_io(self.outputs or [])
            + get_env_io(self.contexts or [])
        )

    def get_io_names(self) -> List[str]:
        def get_io_name(io: List[V1IO]) -> List[str]:
            return [i.name for i in io if i.name]

        return (
            get_io_name(self.inputs or [])
            + get_io_name(self.outputs or [])
            + get_io_name(self.contexts or [])
        )

    def apply_image_destination(self, image: str):
        self.run.apply_image_destination(image)

    @property
    def has_pipeline(self):
        return self.is_dag_run or self.matrix or self.schedule

    def validate_build(self):
        if self.build and self.is_dag_run:
            raise PolyaxonSchemaError(
                "Operations with dag runtime do not support the `build` section."
            )
