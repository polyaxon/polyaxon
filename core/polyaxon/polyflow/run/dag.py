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

from collections import Mapping

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.k8s import k8s_schemas
from polyaxon.pkg import SCHEMA_VERSION
from polyaxon.polyflow import dags
from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.environment import EnvironmentSchema
from polyaxon.polyflow.io import V1IO
from polyaxon.polyflow.io import params as ops_params
from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class DagSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.DAG))
    operations = fields.List(fields.Nested("OperationSchema"))
    components = fields.List(fields.Nested("ComponentSchema"))
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    connections = fields.List(fields.Str(), allow_none=True)
    volumes = fields.List(SwaggerField(cls=k8s_schemas.V1Volume), allow_none=True)
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.List(fields.Nested(EarlyStoppingSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Dag


class V1Dag(BaseConfig, polyaxon_sdk.V1Dag):
    SCHEMA = DagSchema
    IDENTIFIER = V1RunKind.DAG
    REDUCED_ATTRIBUTES = [
        "operations",
        "components",
        "concurrency",
        "earlyStopping",
        "environment",
        "connections",
        "volumes",
    ]

    def __init__(
        self,
        operations=None,
        components=None,
        concurrency=None,
        early_stopping=None,
        kind=None,
        environment=None,
        connections=None,
        volumes=None,
    ):
        super().__init__(
            kind=kind,
            operations=operations,
            components=components,
            concurrency=concurrency,
            early_stopping=early_stopping,
            environment=environment,
            connections=connections,
            volumes=volumes,
        )
        self._dag = {}  # OpName -> DagOpSpec
        self._components_by_names = {}  # ComponentName -> Component
        self._op_component_mapping = {}  # OpName -> ComponentName
        self._context = {}  # Ops output names -> types

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

        if not isinstance(op.params, Mapping):
            raise PolyaxonSchemaError(
                "Op `{}` defines a malformed params `{}`, "
                "params should be a dictionary of form <name: value>".format(
                    op.name, op.params
                )
            )

        for param in op.params:
            param_spec = op.params[param].get_spec(
                name=param, iotype=None, is_flag=None
            )
            if param_spec.param.is_ops_ref:
                upstream.add(param_spec.param.entity_ref)

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
        for op in self.operations or []:
            self._process_op(op)

    def add_op(self, op):
        self.operations = self.operations or []
        self.operations.append(op)
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

        if not self.operations:
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

        for op in self.operations:
            op_name = op.name
            if op.has_component_reference:
                outputs = op.template.outputs
                inputs = op.template.inputs
            elif op.has_dag_reference:
                component_ref_name = op.template.name
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
            elif op.has_hub_reference:
                continue
            elif op.has_url_reference:
                continue
            elif op.has_path_reference:
                continue
            else:
                raise PolyaxonSchemaError(
                    "Pipeline op has no template field `{}`".format(op_name)
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

            # We allow to resolve name, status, project, all outputs/inputs, iteration
            self._context["ops.{}.inputs".format(op_name)] = V1IO(
                name="inputs", iotype=types.DICT, value={}, is_optional=True
            )
            self._context["ops.{}.outputs".format(op_name)] = V1IO(
                name="outputs", iotype=types.DICT, value={}, is_optional=True
            )
            self._context["ops.{}.status".format(op_name)] = V1IO(
                name="status", iotype=types.STR, value="", is_optional=True
            )
            self._context["ops.{}.name".format(op_name)] = V1IO(
                name="name", iotype=types.STR, value="", is_optional=True
            )
            self._context["ops.{}.uuid".format(op_name)] = V1IO(
                name="uuid", iotype=types.STR, value="", is_optional=True
            )
            self._context["ops.{}.project_name".format(op_name)] = V1IO(
                name="project_name", iotype=types.STR, value="", is_optional=True
            )
            self._context["ops.{}.project_uuid".format(op_name)] = V1IO(
                name="project_uuid", iotype=types.STR, value="", is_optional=True
            )
            self._context["ops.{}.iteration".format(op_name)] = V1IO(
                name="iteration", iotype=types.STR, value="", is_optional=True
            )

        for op in self.operations:
            if op.has_component_reference:
                component_ref = op.template.name
                outputs = op.template.outputs
                inputs = op.template.inputs
            elif op.has_hub_reference:
                component_ref = op.template.name
                continue
            elif op.has_url_reference:
                component_ref = op.template.url
                continue
            elif op.has_path_reference:
                component_ref = op.template.path
                continue
            elif op.has_dag_reference:
                component_ref = op.template.name
                outputs = self._components_by_names[component_ref].outputs
                inputs = self._components_by_names[component_ref].inputs
            else:
                raise PolyaxonSchemaError(
                    "Pipeline op has no template field `{}`".format(op.name)
                )
            ops_params.validate_params(
                params=op.params,
                inputs=inputs,
                outputs=outputs,
                context=self._context,
                is_template=False,
                check_runs=False,
                extra_info="<op {}>.<component {}>".format(op.name, component_ref),
            )

    def set_op_component(self, op_name):
        if op_name not in self.dag:
            raise PolyaxonSchemaError(
                "Job with name `{}` was not found in Dag, "
                "make sure to run `process_dag`.".format(op_name)
            )
        op_spec = self.dag[op_name]
        if op_spec.op.has_component_reference:
            return

        if op_name not in self._op_component_mapping:
            raise PolyaxonSchemaError(
                "Pipeline op with name `{}` requires a reference `{} ({})`, "
                "which is not defined on this pipeline, "
                "make sure to run `process_components`".format(
                    op_name,
                    op_spec.op.template.kind,
                    op_spec.op.template.get_kind_value(),
                )
            )
        component_ref_name = self._op_component_mapping[op_name]
        op_spec.op.set_template(self._components_by_names[component_ref_name])

    def get_op_spec_by_index(self, idx):
        from polyaxon.polyaxonfile import OperationSpecification

        op_dict = self.operations[idx].to_dict()
        op_dict[OperationSpecification.VERSION] = op_dict.get(
            OperationSpecification.VERSION, SCHEMA_VERSION
        )
        return OperationSpecification.read(op_dict)

    def get_op_spec_by_name(self, name):
        from polyaxon.polyaxonfile import OperationSpecification

        op_dict = self.dag[name].op.to_dict()
        op_dict[OperationSpecification.VERSION] = op_dict.get(
            OperationSpecification.VERSION, SCHEMA_VERSION
        )
        return OperationSpecification.read(op_dict)
