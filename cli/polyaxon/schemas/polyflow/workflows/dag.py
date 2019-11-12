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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.polyflow import dags
from polyaxon.schemas.polyflow import params as ops_params
from polyaxon.schemas.polyflow.workflows.early_stopping_policies import (
    EarlyStoppingSchema,
)


class DagSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("dag"))
    ops = fields.Nested("OpSchema", many=True)
    components = fields.Nested("ComponentSchema", many=True)
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return DagConfig


class DagConfig(BaseConfig):
    SCHEMA = DagSchema
    IDENTIFIER = "dag"
    REDUCED_ATTRIBUTES = ["ops", "components", "concurrency", "early_stopping"]

    def __init__(
        self,
        ops=None,
        components=None,
        concurrency=None,
        early_stopping=None,
        kind=IDENTIFIER,
    ):
        self.kind = kind
        self.ops = ops
        self.components = components
        self.concurrency = concurrency
        self.early_stopping = early_stopping
        self._dag = {}  # OpName -> DagOpSpec
        self._components_by_names = {}  # ComponentName -> Component
        self._op_component_mapping = {}  # OpName -> ComponentName
        self._context = {}  # Ops output names -> IOTypes

    @property
    def dag(self):
        return self._dag

    def validate_dag(self, dag=None):
        dag = dag or self.dag
        orphan_ops = self.get_orphan_ops(dag=dag)
        if orphan_ops:
            raise PolyaxonSchemaError(
                "Pipeline has a non valid dag, the dag contains an orphan ops: `{}`, "
                "check if you are referencing this op "
                "in a parameter or a condition".format(orphan_ops)
            )
        self.sort_topologically(dag=dag)

    def _get_op_upstream(self, op):
        upstream = set(op.dependencies) if op.dependencies else set([])

        if not op.params:
            return upstream

        for param in op.params:
            param_ref = ops_params.get_param(
                name=param, value=op.params[param], iotype=None, is_flag=None
            )
            if param_ref and param_ref.entity == ops_params.OPS:
                upstream.add(param_ref.entity_ref)

        return upstream

    def _process_op(self, op):
        upstream = self._get_op_upstream(op=op)
        self._dag = dags.set_dag_op(
            dag=self.dag, op_id=op.name, op=op, upstream=upstream, downstream=None
        )
        for op_name in upstream:
            self._dag = dags.set_dag_op(
                dag=self.dag, op_id=op_name, downstream=[op.name]
            )

    def process_dag(self):
        for op in self.ops or []:
            self._process_op(op)

    def add_op(self, op):
        self.ops = self.ops or []
        self.ops.append(op)
        self._process_op(op)

    def add_ops(self, ops):
        for op in ops:
            self.add_op(op)

    def get_independent_ops(self, dag=None):
        """Get a list of all node in the graph with no dependencies."""
        return dags.get_independent_ops(self.dag or dag)

    def get_orphan_ops(self, dag=None):
        """Get orphan ops for given dag."""
        return dags.get_orphan_ops(dag or self.dag)

    def sort_topologically(self, dag=None, flatten=False):
        """Sort the dag breath first topologically.

        Only the nodes inside the dag are returned, i.e. the nodes that are also keys.

        Returns:
             a topological ordering of the DAG.
        Raises:
             an error if this is not possible (graph is not valid).
        """

        return dags.sort_topologically(dag or self.dag, flatten=flatten)

    def process_components(self, inputs=None):
        inputs = inputs or []
        for _input in inputs:
            self._context["dag.inputs.{}".format(_input.name)] = _input

        if not self.ops:
            raise PolyaxonSchemaError(
                "Pipeline is not valid, it has no ops to validate components."
            )

        components = self.components or []

        for component in components:
            component_name = component.name
            if component_name in self._components_by_names:
                raise PolyaxonSchemaError(
                    "Pipeline has multiple components with the same name `{}`".format(
                        component_name
                    )
                )
            self._components_by_names[component_name] = component

        for op in self.ops:
            op_name = op.name
            if op.component:
                outputs = op.component.outputs
                inputs = op.component.inputs
            elif op.component_ref and op.component_ref.name:
                component_ref_name = op.component_ref.name
                if op_name in self._op_component_mapping:
                    raise PolyaxonSchemaError(
                        "Pipeline has multiple ops with the same name `{}`".format(
                            op_name
                        )
                    )
                if component_ref_name not in self._components_by_names:
                    raise PolyaxonSchemaError(
                        "Pipeline op with name `{}` requires a component with name `{}`, "
                        "which is not defined on this pipeline.".format(
                            op_name, component_ref_name
                        )
                    )
                self._op_component_mapping[op_name] = component_ref_name
                outputs = self._components_by_names[component_ref_name].outputs
                inputs = self._components_by_names[component_ref_name].inputs
            elif op.component_ref.hub:
                continue
            else:
                raise PolyaxonSchemaError(
                    "Pipeline op has no component or component_ref `{}`".format(op_name)
                )

            if outputs:
                for output in outputs:
                    self._context[
                        "ops.{}.outputs.{}".format(op_name, output.name)
                    ] = output

            if inputs:
                for cinput in inputs:
                    self._context[
                        "ops.{}.inputs.{}".format(op_name, cinput.name)
                    ] = cinput

        for op in self.ops:
            if op.component:
                outputs = op.component.outputs
                inputs = op.component.inputs
            elif op.component_ref.hub:
                continue
            else:
                outputs = self._components_by_names[op.component_ref.name].outputs
                inputs = self._components_by_names[op.component_ref.name].inputs
            ops_params.validate_params(
                params=op.params,
                inputs=inputs,
                outputs=outputs,
                context=self._context,
                is_template=False,
                check_runs=False,
                extra_info="<op {}>.<component {}>".format(
                    op.name,
                    op.component.name if op.component else op.component_ref.name,
                ),
            )

    def set_op_component(self, op_name):
        if op_name not in self.dag:
            raise PolyaxonSchemaError(
                "Job with name `{}` was not found in Dag, "
                "make sure to run `process_dag`.".format(op_name)
            )
        op_spec = self.dag[op_name]
        if op_spec.op.component:
            return

        if op_name not in self._op_component_mapping:
            raise PolyaxonSchemaError(
                "Pipeline op with name `{}` requires a component_ref with name `{}`, "
                "which is not defined on this pipeline, "
                "make sure to run `process_components`".format(
                    op_name, op_spec.op.component_ref.name
                )
            )
        component_ref_name = self._op_component_mapping[op_name]
        op_spec.op.component = self._components_by_names[component_ref_name]

        # # Check version
        # if op_spec.op.component.version is None:
        #     op_spec.op.component.version = version or VERSION
        # if op_spec.op.version is None:
        #     op_spec.op.version = self.version
        # # Check op has kind
        # if op_spec.op.kind is None:
        #     op_spec.op.kind = kinds.COMPONENT
