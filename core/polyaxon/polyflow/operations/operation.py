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

import polyaxon_sdk

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.polyflow.component.component import ComponentSchema
from polyaxon.polyflow.operations.base import BaseOp, BaseOpSchema
from polyaxon.polyflow.params import ParamSchema
from polyaxon.polyflow.references import V1DagRef, V1HubRef, V1PathRef, V1UrlRef
from polyaxon.polyflow.run.patch import validate_run_patch


class OperationSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("operation"))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )
    run_patch = fields.Dict(keys=fields.Str(), values=fields.Raw(), allow_none=True)
    hub_ref = fields.Str(allow_none=True)
    dag_ref = fields.Str(allow_none=True)
    url_ref = fields.Str(allow_none=True)
    path_ref = fields.Str(allow_none=True)
    component = fields.Nested(ComponentSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Operation

    @validates_schema
    def validate_run_patch(self, data, **kwargs):
        component = data.get("component")
        run_patch = data.get("run_patch")
        if not component or not run_patch:
            return

        validate_run_patch(run_patch=run_patch, kind=component.run.kind)

    @validates_schema
    def validate_reference(self, data, **kwargs):
        count = 0
        hub_ref = data.get("hub_ref")
        if hub_ref:
            count += 1
        dag_ref = data.get("dag_ref")
        if dag_ref:
            count += 1
        url_ref = data.get("url_ref")
        if url_ref:
            count += 1
        path_ref = data.get("path_ref")
        if path_ref:
            count += 1
        component = data.get("component")
        if component and count == 0:
            count += 1

        if count != 1:
            raise ValidationError(
                "One and only one reference must be specified: "
                "hub_ref, dag_ref, url_ref, path_ref, component."
            )


class V1Operation(BaseOp, polyaxon_sdk.V1Operation):
    """An operation is how Polyaxon executes a component by passing parameters,
    connections, and a run environment.

    With an operation users can:
     * Pass the parameters for required inputs or override the default values of optional inputs.
     * Patch the definition of the component to set environments, initializers, and resources.
     * Set termination logic and retries.
     * Set trigger logic to start a component in a pipeline context.
     * Parallelize or map the component over a matrix of parameters.
     * Put an operation on a schedule.
     * Subscribe a component to events to trigger executions automatically.

    Args:
        version: str
        kind: str, should be equal to `operation`
        name: str, optional
        description: str, optional
        tags: List[str], optional
        profile: str, optional
        queue: str, optional
        cache: [V1Cache](/docs/automation/helpers/cache/), optional
        termination: [V1Termination](/docs/core/specification/termination/), optional
        plugins: [V1Plugins](/docs/core/specification/plugins/), optional
        params: Dict[str, [V1Param](/docs/core/specification/params/)], optional
        schedule: Union[[V1CronSchedule](/docs/automation/schedules/cron/)
                  [V1IntervalSchedule](/docs/automation/schedules/interval/),
                  [V1RepeatableSchedule](/docs/automation/schedules/repeatable/),
                  [V1ExactTimeSchedule](/docs/automation/schedules/exact-time/)], optional
        events: [events](/docs/automation/optimization-engine/events/),
                optional
        matrix: Union[[V1Mapping](/docs/automation/mapping/),
                  [V1GridSearch](/docs/automation/optimization-engine/grid-search/),
                  [V1RandomSearch](/docs/automation/optimization-engine/random-search/),
                  [V1Hyperband](/docs/automation/optimization-engine/hyperband/),
                  [V1Bayes](/docs/automation/optimization-engine/bayesian-optimization/),
                  [V1Hyperopt](/docs/automation/optimization-engine/hyperopt/),
                  [V1Iterative](/docs/automation/optimization-engine/iterative/)], optional
        dependencies:
            [dependencies](/docs/automation/flow-engine/specification/#dependencies),
            optional
        trigger: [trigger](/docs/automation/flow-engine/specification/#trigger),
                 optional
        conditions: [conditions](/docs/automation/flow-engine/specification/#conditions),
                    optional
        skip_on_upstream_skip:
            [skip_on_upstream_skip](/docs/automation/flow-engine/skiponupstreamskip/),
            optional
        run_patch: Dict, optional
        hub_ref: str, optional
        dag_ref: str, optional
        url_ref: str, optional
        path_ref: str, optional
        component: [V1Component](/docs/core/specification/component/), optional

    ## YAML usage

    ```yaml
    >>> operation:
    >>>   version: 1.1
    >>>   kind: operation
    >>>   name:
    >>>   description:
    >>>   tags:
    >>>   profile:
    >>>   queue:
    >>>   cache:
    >>>   termination:
    >>>   plugins:
    >>>   params:
    >>>   runPatch:
    >>>   hubRef:
    >>>   dagRef:
    >>>   dagRef:
    >>>   component:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Cache, V1Component, V1Param, V1Plugins, V1Operation, V1Termination
    >>> operation = V1Operation(
    >>>     name="test",
    >>>     description="test",
    >>>     tags=["test"],
    >>>     profile="test",
    >>>     queue="test",
    >>>     cache=V1Cache(...),
    >>>     termination=V1Termination(...),
    >>>     plugins=V1Plugins(...),
    >>>     outputs={"param1": V1Param(...), ...},
    >>>     component=V1Component(...),
    >>> )
    ```

    ## Fields

    ### version

    The polyaxon specification version to use to validate the operation.

    ```yaml
    >>> operation:
    >>>   version: 1.1
    ```

    ### kind

    The kind signals to the CLI, client, and other tools that this is an operation.

    If you are using the python client to create an operation,
    this field is not required and is set by default.

    ```yaml
    >>> operation:
    >>>   kind: component
    ```

    ### name

    The name to use for this operation run,
    if provided, it will override the component's name otherwise
    the name of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   name: test
    ```

    ### description

    The description to use for this operation run,
    if provided, it will override the component's description otherwise
    the description of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   description: test
    ```

    ### tags

    The tags to use for this operation run,
    if provided, it will override the component's tags otherwise
    the tags of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   tags: [test]
    ```

    ### profile

    The [run profile](/docs/management/ui/run-profiles/) to use for this operation run,
    if provided, it will override the component's profile otherwise
    the profile of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   profile: test
    ```

    ### queue

    The [queue](/docs/core/scheduling-strategies/queue-routing/) to use for this operation run,
    if provided, it will override the component's queue otherwise
    the queue of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   queue: test
    ```

    ### cache

    The [cache](/docs/automation/helpers/cache/) to use for this operation run,
    if provided, it will override the component's cache otherwise
    the cache of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   cache:
    >>>     disable: false
    >>>     ttl: 100
    ```

    ### termination

    The [termination](/docs/core/specification/termination/) to use for this operation run,
    if provided, it will override the component's termination otherwise
    the termination of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   termination:
    >>>     maxRetries: 2
    ```

    ### plugins

    The [plugins](/docs/core/specification/plugins/) to use for this operation run,
    if provided, it will override the component's plugins otherwise
    the plugins of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   name: debug
    >>>   ...
    >>>   plugins:
    >>>     auth: false
    >>>     collectLogs: false
    >>>   ...
    ```

    ### params

    The [params](/docs/core/specification/params/)  to pass to the component,
    they will be validated against the inputs / outputs.
    If a param is passed and the component does not define a corresponding inputs / outputs,
    a validation error will be raised unless the param is has the contextOnly flag enabled.

    ```yaml
    >>> operation:
    >>>   params:
    >>>     param1: {value: 1.1}
    >>>     param2: {value: test}
    >>>     param3: {ref: ops.upstream-operation, value: outputs.metric}
    >>>   ...
    ```

    ### run_patch

    The run patch provide a way to override information about the component's run section,
    for example the container's resources or the environment section.

    The run patch is a dictionary that can modify most of the run time information and
    will be resolved against the corresponding run kind:

        * [V1Job](/docs/experimentation/jobs/): for running batch jobs, model training experiments,
                                                data processing jobs, ...
        * [V1Service](/docs/experimentation/services/): for running tensorboards, notebooks,
                                                        streamlit, custom services or an API.
        * [V1TFJob](/docs/experimentation/distributed/tf-jobs/): for running distributed
                                                                 Tensorflow training job.
        * [V1PytorchJob](/docs/experimentation/distributed/pytorch-jobs/): for running distributed
                                                                           Pytorch training job.
        * [V1MPIJob](/docs/experimentation/distributed/mpi-jobs/): for running distributed
                                                                   MPI job.
        * [V1Spark](/docs/experimentation/distributed/spark-jobs/): for running a spark Application.
        * [V1Dask](/docs/experimentation/distributed/dask-jobs/): for running a Dask job.
        * [V1Dag](/docs/automation/flow-engine/specification/): for running a DAG / workflow.

    For example, fi we define a generic component for running Jupyter Notebook:

    ```yaml
    >>> version: 1.1
    >>> kind: component
    >>> name: notebook
    >>> run:
    >>>   kind: service
    >>>   ports: [8888]
    >>>   container:
    >>>     image: "jupyter/tensorflow-notebook"
    >>>     command: ["jupyter", "lab"]
    >>>     args: [
    >>>       "--no-browser",
    >>>       "--ip=0.0.0.0",
    >>>       "--port={{globals.ports[0]}}",
    >>>       "--allow-root",
    >>>       "--NotebookApp.allow_origin=*",
    >>>       "--NotebookApp.trust_xheaders=True",
    >>>       "--NotebookApp.token=",
    >>>       "--NotebookApp.base_url={{globals.base_url}}",
    >>>       "--LabApp.base_url={{globals.base_url}}"
    >>>     ]
    ```

    This component is generic, and does not define resources requirements,
    if for instance this component is hosted on github and you don't
    want to modify the component while at the sametime you want to request a GPU for the notebook,
    you can patch the run:

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> urlRef: https://raw.githubusercontent.com/org/repo/master/components/notebook.yaml
    >>> runPatch:
    >>>   container:
    >>>     resources:
    >>>       limits:
    >>>         nvidia.com/gpu: 1
    ```

    By applying a run patch you can effectively share components while having
    full control over customizable details.

    ### hub_ref

    Polyaxon provides a [Component Hub](/docs/management/component-hub/)
    for hosting versioned components with access control system to improve
    the productivity of your team.

    To run a component hosted on Polyaxon Component Hub, you can use `hubRef`

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> hubRef: myComponent:v1.1
    ...
    ```

    ### dag_ref

    If you building a dag and you have a component that can be used by several operation,
    you can define a component and reuse it in all operations using `dagRef`.
    Please check Polyaxon automation's [flow engine section](/docs/automation/flow-engine/)
    for more details.

    ### url_ref

    You can host your components on an accessible url, e.g github,
    and reference those components without downloading the data manually.

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> urlRef: https://raw.githubusercontent.com/org/repo/master/components/my-component.yaml
    ...
    ```

    > Please note that you can only use this reference when using the CLI tool.

    ### path_ref

    In many situations, components can be placed in different folders within a project, e.g.
    data-processing, data-exploration, ml-modeling, ...

    You can define operations without the need to change
    the directory by referencing a path to that component:

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> pathRef: ../data-processing/component-clean.yaml
    ...
    ```

    > Please note that you can only use this reference when using the CLI tool.

    ### component

    If you are still in the developement phase or if you are building a
    singleton operation that can be executed in a unique way, you can define
    the component inline inside the operation:

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> component:
    >>>   run:
    >>>      kind: job
    >>>      container:
    >>>        image: foo:latest
    >>>        command: train --lr=0.01
    ...
    ```
    """

    SCHEMA = OperationSchema
    IDENTIFIER = "operation"
    REDUCED_ATTRIBUTES = BaseOp.REDUCED_ATTRIBUTES + [
        "params",
        "hubRef",
        "dagRef",
        "urlRef",
        "pathRef",
        "component",
        "runPatch",
    ]

    @property
    def has_component_reference(self) -> bool:
        return self.component is not None

    @property
    def has_dag_reference(self) -> bool:
        return bool(self.dag_ref)

    @property
    def has_hub_reference(self) -> bool:
        return bool(self.hub_ref)

    @property
    def has_public_hub_reference(self) -> bool:
        if not self.has_hub_reference:
            return False
        return "/" not in self.hub_ref

    @property
    def has_path_reference(self) -> bool:
        return bool(self.path_ref)

    @property
    def has_url_reference(self) -> bool:
        return bool(self.url_ref)

    @property
    def reference(self):
        if self.has_component_reference:
            return self.component
        if self.has_dag_reference:
            return V1DagRef(name=self.dag_ref)
        if self.has_hub_reference:
            return V1HubRef(name=self.hub_ref)
        if self.has_path_reference:
            return V1PathRef(path=self.path_ref)
        if self.has_url_reference:
            return V1UrlRef(url=self.url_ref)

    @property
    def template(self):
        if self.has_component_reference:
            return self.component
        if self.has_dag_reference:
            return V1DagRef(name=self.dag_ref)
        if self.has_hub_reference:
            return V1HubRef(name=self.hub_ref)
        if self.has_path_reference:
            return V1PathRef(path=self.path_ref)
        if self.has_url_reference:
            return V1UrlRef(url=self.url_ref)

    def set_template(self, value):
        self.component = value
