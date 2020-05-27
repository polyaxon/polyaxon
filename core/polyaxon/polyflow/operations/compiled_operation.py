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
from typing import List

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.io import IOSchema
from polyaxon.polyflow.operations.base import BaseOp, BaseOpSchema
from polyaxon.polyflow.params import ParamSpec, ops_params
from polyaxon.polyflow.run import RunMixin, RunSchema


class CompiledOperationSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("compiled_operation"))
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)
    run = fields.Nested(RunSchema, required=True)

    @staticmethod
    def schema_config():
        return V1CompiledOperation


class V1CompiledOperation(BaseOp, RunMixin, polyaxon_sdk.V1CompiledOperation):
    SCHEMA = CompiledOperationSchema
    IDENTIFIER = "compiled_operation"
    REDUCED_ATTRIBUTES = BaseOp.REDUCED_ATTRIBUTES + ["inputs", "outputs", "run"]

    def get_run_kind(self):
        return self.run.kind if self.run else None

    def validate_params(
        self, params=None, context=None, is_template=True, check_runs=False
    ) -> List[ParamSpec]:
        return ops_params.validate_params(
            inputs=self.inputs,
            outputs=self.outputs,
            params=params,
            matrix=self.matrix,
            context=context,
            is_template=is_template,
            check_runs=check_runs,
        )

    def apply_params(self, params=None, context=None):
        context = context or {}
        validated_params = self.validate_params(
            params=params, context=context, is_template=False, check_runs=True
        )
        if not validated_params:
            return

        param_specs = {}
        for param in validated_params:
            param_specs[param.name] = param

        def set_io(io):
            if not io:
                return
            for i in io:
                if i.name in param_specs:
                    i.is_optional = True
                    if param_specs[i.name].param.is_literal:
                        i.value = param_specs[i.name].param.value

        set_io(self.inputs)
        set_io(self.outputs)

    @property
    def has_pipeline(self):
        return self.is_dag_run or self.matrix
