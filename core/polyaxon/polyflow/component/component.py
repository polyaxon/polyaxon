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

from marshmallow import fields, validate

from polyaxon.polyflow.component.base import BaseComponent, BaseComponentSchema
from polyaxon.polyflow.io import IOSchema
from polyaxon.polyflow.references import RefMixin
from polyaxon.polyflow.run import RunMixin, RunSchema
from polyaxon.polyflow.templates import TemplateMixinConfig, TemplateMixinSchema
from polyaxon.schemas.base import NAME_REGEX


class ComponentSchema(BaseComponentSchema, TemplateMixinSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("component"))
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)
    run = fields.Nested(RunSchema, required=True)

    @staticmethod
    def schema_config():
        return V1Component


class V1Component(
    BaseComponent, TemplateMixinConfig, RunMixin, RefMixin, polyaxon_sdk.V1Component
):
    """Component is a discrete, repeatable, and self-contained action that defines
    an environment and a runtime.

    A component is made of code that performs an action,
    such as container building, data preprocessing, data transformation, model training, and so on.

    You can use any language to write the logic of your component,
    Polyaxon uses containers to execute that logic.

    Components are definitions that can be shared if they reach a
    certain maturity and can be managed by the [Component Hub](/docs/management/component-hub/).
    This allows you to create a library of frequently-used components and reuse them
    either by submitting them directly or by referencing them from your operations.

    Components can be used as well to extract as much information and be used as templates
    with default queues, container resources requirements, node scheduling, ...

    Args:
        version: str
        kind: str, should be equal to `component`
        name: str, optional
        description: str, optional
        tags: List[str], optional
        presets: List[str], optional
        queue: str, optional
        cache: [V1Cache](/docs/automation/helpers/cache/), optional
        termination: [V1Termination](/docs/core/specification/termination/), optional
        plugins: [V1Plugins](/docs/core/specification/plugins/), optional
        actions: List[[V1Action](/docs/automation/extensions/actions/)], optional
        hooks: List[[V1Hook](/docs/automation/extensions/hooks/)], optional
        inputs: [V1IO](/docs/core/specification/io/), optional
        outputs: [V1IO](/docs/core/specification/io/), optional
        run: Union[[V1Job](/docs/experimentation/jobs/),
             [V1Service](/docs/experimentation/services/),
             [V1TFJob](/docs/experimentation/distributed/tf-jobs/),
             [V1PytorchJob](/docs/experimentation/distributed/pytorch-jobs/),
             [V1MPIJob](/docs/experimentation/distributed/mpi-jobs/),
             [V1Spark](/docs/experimentation/distributed/spark-jobs/),
             [V1Dask](/docs/experimentation/distributed/dask-jobs/),
             [V1Dag](/docs/automation/flow-engine/specification/)]
        template: [V1Template](/docs/core/specification/template/), optional

    ## YAML usage

    ```yaml
    >>> component:
    >>>   version: 1.1
    >>>   kind: component
    >>>   name:
    >>>   description:
    >>>   tags:
    >>>   presets:
    >>>   queue:
    >>>   cache:
    >>>   termination:
    >>>   plugins:
    >>>   actions:
    >>>   hooks:
    >>>   inputs:
    >>>   outputs:
    >>>   run:
    >>>   template:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Cache, V1Component, V1IO, V1Plugins, V1Termination
    >>> component = V1Component(
    >>>     name="test",
    >>>     description="test",
    >>>     tags=["test"],
    >>>     presets=["test"],
    >>>     queue="test",
    >>>     cache=V1Cache(...),
    >>>     termination=V1Termination(...),
    >>>     plugins=V1Plugins(...),
    >>>     actions=[V1Action(...)],
    >>>     hooks=[V1Hook(...)],
    >>>     inputs=V1IO(...),
    >>>     outputs=V1IO(...),
    >>>     run=...
    >>> )
    ```

    ## Fields

    ### version

    The polyaxon specification version to use to validate the component.

    If you are using the component inline in an operation, this field is not required since it
    will be populated by the operation.

    ```yaml
    >>> component:
    >>>   version: 1.1
    ```

    ### kind

    The kind signals to the CLI, client, and other tools that this is a component.

    If you are using the component inline in an operation or a dag or
    if you are using the python client to create a component,
    this field is not required and is set by default.

    ```yaml
    >>> component:
    >>>   kind: component
    ```

    ### name

    The default component name.

    This name can be a `slug`, a `slug:tag`, `org/slug`, or `org/slug:slug`.

    This name will be passed as the default value to all operations using this component,
    unless the operations override the name or a `--name`
    is passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   name: test
    ```

    ### description

    The default component description.

    This description will be passed as the default value to all operations using this component,
    unless the operations override the description or a
    `--description` is passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   description: test
    ```

    ### tags

    The default component tags.

    These tags will be passed as the default value to all operations using this component,
    unless the operations override the tags or `--tags` are passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   tags: [test]
    ```

    ### presets

    The default component [presets](/docs/core/scheduling-strategies/presets/).

    These presets will be passed as the default value to all operations using this component,
    unless the operations override the presets or `--presets`
    is passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   presets: [test]
    ```

    ### queue

    The default component [queue](/docs/core/scheduling-strategies/queue-routing/).

    This queue will be passed as the default value to all operations using this component,
    unless the operations override the queue or `--queue`
    is passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   queue: agent-name/queue-name
    ```

    If the agent name is not specified, Polyaxon will resolve the name of the queue
    based on the default agent.

    ```yaml
    >>> component:
    >>>   queue: queue-name
    ```

    ### cache

    The default component [cache](/docs/automation/helpers/cache/).

    This cache definition will be passed as the default value to
    all operations using this component,
    unless the operations override the cache or `--nocache`
    is passed as an argument to the cli/client.

    ```yaml
    >>> component:
    >>>   cache:
    >>>     disable: false
    >>>     ttl: 100
    ```

    ### termination

    The default component [termination](/docs/core/specification/termination/).

    This termination definition will be passed as the default value to
    all operations using this component,
    unless the operations override the termination.

    ```yaml
    >>> component:
    >>>   termination:
    >>>     maxRetries: 2
    ```

    ### plugins

    The default component [plugins](/docs/core/specification/plugins/).

    This plugins definition will be passed as the default value to
    all operations using this component,
    unless the operations override the plugins.

    ```yaml
    >>> component:
    >>>   name: debug
    >>>   ...
    >>>   plugins:
    >>>     auth: false
    >>>     collectLogs: false
    >>>   ...
    ```

    Build using docker:

    ```yaml
    >>> component:
    >>>   name: build
    >>>   ...
    >>>   plugins:
    >>>     docker: true
    >>>   ...
    ```

    ### inputs

    The [inputs](/docs/core/specification/io/) definition for this component.

    If the component defines required inputs, anytime a user tries to run
    this component without passing the required params or passing params with wrong types,
    an exception will be raised.

    ```yaml
    >>> component:
    >>>   name: tensorboard
    >>>   ...
    >>>   inputs:
    >>>     - name: image
    >>>       type: str
    >>>       isOptional: true
    >>>       value: tensorflow:2.1
    >>>     - name: log_dir
    >>>       type: path
    >>>   ...
    ```

    ### outputs

    The [outputs](/docs/core/specification/io/) definition for this component.

    If the component defines required outputs, no exception will be raised at execution time,
    since Polyaxon considers the outputs values will be resolved in the future,
    for example during the run time when the user will be using the tracking
    client to log a metric or a value or an artifact.

    Sometimes the outputs can be resolved immediately at execution time,
    for example a container image name, because such information is required for the
    job to finish successfully, i.e. pushing the image with the correct name,
    in that case you can disable `delayValidation` flag.

    ```yaml
    >>> component:
    >>>   name: tensorboard
    >>>   ...
    >>>   outputs:
    >>>     - name: image
    >>>       type: str
    >>>       delayValidation: false
    >>>   ...
    ```

    ### run

    This is the section that defines the runtime of the component:
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
        * [V1Dag](/docs/automation/flow-engine/specification/): for running a DAG/workflow.
    """

    SCHEMA = ComponentSchema
    IDENTIFIER = "component"
    REDUCED_ATTRIBUTES = (
        BaseComponent.REDUCED_ATTRIBUTES
        + TemplateMixinConfig.REDUCED_ATTRIBUTES
        + ["inputs", "outputs", "run"]
    )

    def get_run_kind(self):
        return self.run.kind if self.run else None

    def get_kind_value(self):
        return self.name

    def get_run_dict(self):
        config_dict = self.to_light_dict()
        config_dict.pop("tag", None)
        return config_dict

    def get_name(self):
        return self.name.split(":")[0] if self.name else None
