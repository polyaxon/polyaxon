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
from typing import Set

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
from polyaxon.polyflow.params import ops_params
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
    """Dag (Directed Acyclic Graphs) is
    a collection of all the operations you want to run,
    organized in a way that reflects their relationships and dependencies.

    A dag's main goal is to describe and run several operations
    necessary for a Machine Learning (ML) workflow.

    A dag executes a dependency graph of operations, each operation runs a Kubernetes privmitive
    described in its component.

    Dags are defined in Polyaxon as a [component runtime](/docs/core/specification/component/#run),
    which makes them compatible with all knowledge used for running other runtimes:
      * They can be defined in reusable components and can be registered in the Component Hub.
      * They get executed using operations.
      * They can be parametrised similar to jobs and services.
      * Since they are defined as components' runtimes, and they run a graph of other components,
        they can be nested natively.
      * They can leverage all [pipeline helpers](/docs/automation/helpers/).
      * They can run in parallel and can be used with [mapping](/docs/automation/mapping/) or
        other [optimization algorithms](/docs/automation/optimization-engine/).
      * They can run on [schedule](/docs/automation/schedules/)
      * They can subscribe to [events](/docs/automation/events/)
      * They can take advantage of all scheduling strategies to route operations to nodes,
        namespaces, and clusters even within the same DAG.

    Args:
        kind: str, should be equal `dag`
        operations: List[[V1Operation](/docs/core/specification/operation/)]
        components: List[[V1Operation](/docs/core/specification/component/)], optional
        environment: [V1Environment](/docs/core/specification/environment/), optional
        connections: List[str], optional
        volumes: List[[Kubernetes Volume](https://kubernetes.io/docs/concepts/storage/volumes/)],
                 optional
        concurrency: init, optional
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   operations:
    >>>   components:
    >>>   environment:
    >>>   connections:
    >>>   volumes:
    >>>   concurrency:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Dag, V1Component, V1Environment, V1Operation
    >>> from polyaxon.k8s import k8s_schemas
    >>> dag = V1Dag(
    >>>     operations=[V1Operation(...)],
    >>>     components=[V1Component(...), V1Component(...)],
    >>>     environment=V1Environment(...),
    >>>     connections=["connection-name1"],
    >>>     volumes=[k8s_schemas.V1Volume(...)],
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this component's runtime is a dag.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: dag
    ```

    ### operations

    A List of operations to run with their dependency definition.
    If the operations are defined with no dependencies or no params are
    passed from one operation to another, the operations will be running in parallel following the
    concurrency and other queue priority definitions.

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   operations:
    >>>     - name: job1
    >>>       hubRef: component1:latest
    >>>       params:
    >>>         ...
    >>>     - name: job2
    >>>       hubRef: component1:2.1
    >>>       params:
    >>>         ...
    >>>     - name: job3
    >>>       urlRef: https://some_url.com
    >>>       params:
    >>>         param1:
    >>>           ref: ops.job2
    >>>           value: outputs.outputName
    >>>
    ```

    #### dependencies

    Dags expose 2 ways to define dependencies between operations:
     * Using the `dependencies` field.
     * Using a parameter reference.

    In addition to the `dependencies` definition, users can add trigger and conditions
    to perform extra checks on the state of those dependencies.

    If an operation must wait for another operation and does not expect
    any parameters from that operation, you can define the dependency manually:

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   operations:
    >>>     - name: job1
    >>>       hubRef: component1:latest
    >>>       params:
    >>>         ...
    >>>     - name: job2
    >>>       hubRef: component1:2.1
    >>>       params:
    >>>         ...
    >>>     - name: job3
    >>>       urlRef: https://some_url.com
    >>>       dependencies: [job1, job2]
    ```

    The job1 and job2 will run in parallel and job3 will wait for both jobs to finish.

    #### params dependencies

    If an operation is expecting a parameter from upstream operations,
    we don't need to define the dependency since it will be inferred from the params definition.

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   operations:
    >>>     - name: job1
    >>>       hubRef: component1:latest
    >>>       params:
    >>>         ...
    >>>     - name: job2
    >>>       hubRef: component1:2.1
    >>>       params:
    >>>         ...
    >>>     - name: job3
    >>>       urlRef: https://some_url.com
    >>>       dependencies: [job1]
    >>>       params:
    >>>         image:
    >>>           ref: ops.job2
    >>>           value: outputs.results
    ```

    This is similar to the previous `dependencies` definition in the sense that
    the job1 and job2 will run in parallel and job3 will wait for both jobs to finish.

    The dependency between job2 and job3 is inferred from the params definition.

    #### trigger

    In order to define a trigger condition or how to trigger job3 based on the status job1 and job2,
    we can use the `trigger` field.
    It determines if a task should run based on the statuses of the upstream tasks.

    ```yaml
    >>> - name: job3
    >>>   urlRef: https://some_url.com
    >>>   dependencies: [job1, job2]
    >>>   trigger: all_succeeded
    ```

    Possible values: `all_succeeded`, `all_failed`, `all_done`,
        `one_succeeded`, `one_failed`, `one_done`

    #### skipOnUpstreamSkip

    if True, if any immediately upstream tasks are skipped,
    this task will automatically be skipped as well, regardless of other conditions or trigger.
    By default, this prevents tasks from attempting to use an incomplete context
    that won't be populated from the upstream tasks that didn't run.
    If False, the task's trigger will be used with any skipped operations considered successes.

    ```yaml
    >>> - name: job3
    >>>   urlRef: https://some_url.com
    >>>   dependencies: [job1, job2]
    >>>   trigger: all_succeeded
    >>>   skipOnUpstreamSkip: true
    ```

    #### conditions

    Conditions are an advance tool for resolving dependencies between operations.
    Conditions take advantage of information resolved in the context to decide if an operation
    can be started, and they can be used to define branching strategies.


    ```yaml
    >>> - name: job3
    >>>   urlRef: https://some_url.com
    >>>   dependencies: [job1]
    >>>   params:
    >>>     image:
    >>>       ref: ops.job2
    >>>       value: outputs.results
    >>>   conditions: '{{ image == "some-value" }}'
    >>>   skipOnUpstreamSkip: true
    ```

    In the example above, the job3 will only run if the param passed is equal to "some-value".

    ### references

    A List of operations and their dependency definition.
    If operations are defined with dependencies or no params are
    passed from one operation to another, the operations will be running in parallel following the
    concurrency and other queue priority definitions.

    Operations can reference components using:
        * [dagRef](/docs/core/specification/operation/#hub_ref)
            (reusable component defined inside the dag)
        * [hubRef](/docs/core/specification/operation/#hub_ref)
        * [pathRef](/docs/core/specification/operation/#path_ref)
        * [urlRef](/docs/core/specification/operation/#url_ref)
        * [inline component](/docs/core/specification/operation/#component)

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   operations:
    >>>     - name: download1
    >>>     dagRef: download
    >>>     params:
    >>>       url: {value: 'gs://ml-pipeline-playground/shakespeare1.txt'}
    >>>       result: {value: 'result.txt'}
    >>>     - name: download2
    >>>       dagRef: download
    >>>       params:
    >>>         url: {value: 'gs://ml-pipeline-playground/shakespeare2.txt'}
    >>>         result: {value: 'result.txt'}
    ```

    ### components

    A list of reusable components defined inside the DAG that can be used by one
    or several operations. This field is only useful when you need to define inline components
    for your operations and more than one operation is using the same component definition.

    ```yaml
    >>> operations:
    >>>   - name: download-url1
    >>>     dagRef: download
    >>>     ...
    >>>   - name: download-url2
    >>>     dagRef: download
    >>>     ...
    >>> components:
    >>>   - name: download
    >>>     inputs:
    >>>       - name: url
    >>>         type: url
    >>>     outputs:
    >>>       - name: result
    >>>         type: path
    >>>         delayValidation: false
    >>>     run:
    >>>       kind: job
    >>>       container:
    >>>         image: 'google/cloud-sdk:272.0.0'
    >>>         command: ['sh', '-c'],
    >>>         args: ['gsutil cat $0 | tee $1', "{{ url }}", "{{ outputs_path }}/{{ result }}"]
    ```

    ### environment

    Optional [environment section](/docs/core/specification/environment/),
    it provides a way to inject pod related information.

    The environment definition will be passed to all children operations.

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   environment:
    >>>     labels:
    >>>        key1: "label1"
    >>>        key2: "label2"
    >>>      annotations:
    >>>        key1: "value1"
    >>>        key2: "value2"
    >>>      nodeSelector:
    >>>        node_label: node_value
    >>>      ...
    >>>  ...
    ```

    ### connections

    A list of [connection names](/docs/setup/connections/) to resolve for the dag.

    <blockquote class="light">
    If you are referencing a connection it must be configured.
    All referenced connections will be checked:

     * If they are accessible in the context of the project of this run

     * If the user running the operation can have access to those connections
    </blockquote>

    The connections definition will be passed to all operations.
    After checks, the connections will be resolved and inject any volumes, secrets, configMaps,
    environment variables for your main container to function correctly.

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   connections: [connection1, connection2]
    ```

    ### volumes

    A list of [Kubernetes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
    to resolve and mount for your jobs.

    This is an advanced use-case where configuring a connection is not an option.

    the volumes definition will be passed to all operations.

    When you add a volume you need to mount it manually to your container(s).

    ```yaml
    >>> run:
    >>>   kind: dag
    >>>   volumes:
    >>>     - name: volume1
    >>>       persistentVolumeClaim:
    >>>       claimName: pvc1
    >>>   ...
    ```
    ### concurrency

    An optional value to set the number of concurrent operations.

    ```yaml
    >>> matrix:
    >>>   kind: dag
    >>>   concurrency: 2
    ```

    For more details about concurrency management,
    please check the [concurrency section](/docs/automation/helpers/concurrency/).

    ### earlyStopping

    A list of early stopping conditions to check for terminating
    all operations managed by the pipeline.
    If one of the early stopping conditions is met,
    a signal will be sent to terminate all running and pending operations.

    ```yaml
    >>> matrix:
    >>>   kind: dag
    >>>   earlyStopping: ...
    ```

    For more details please check the
    [early stopping section](/docs/automation/helpers/early-stopping/).

    """

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
        # This is only usable from cli, the full op must be resolved before it can be submitted
        self._path_context = None

    def set_path_context(self, path_context):
        self._path_context = path_context

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

    def _get_op_upstream(self, op) -> Set:
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
                name=param, iotype=None, is_flag=None, is_list=None
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
        from polyaxon.polyaxonfile.check import collect_references

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
            if op.has_url_reference or op.has_path_reference:
                try:
                    op = collect_references(op, self._path_context)
                except Exception as e:
                    raise PolyaxonSchemaError(
                        "Pipeline op with name `{}` requires a component with ref `{}`, "
                        "the reference could not be resolved. Error: {}".format(
                            op_name, op.hub_ref or op.url_ref or op.path_ref, e
                        )
                    )
            elif op.has_hub_reference:
                continue
            if op.has_component_reference:
                outputs = op.component.outputs
                inputs = op.component.inputs
            elif op.has_dag_reference:
                component_ref_name = op.dag_ref
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
            if op.has_hub_reference:
                continue
            elif op.has_component_reference:
                component_ref = op.template.name
                outputs = op.template.outputs
                inputs = op.template.inputs
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
                matrix=op.matrix,
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
