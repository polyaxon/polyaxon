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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.cache import CacheSchema
from polyaxon.polyflow.params import ParamSchema
from polyaxon.schemas import V1PatchStrategy
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class BuildSchema(BaseCamelSchema):
    hub_ref = fields.Str(required=True)
    connection = fields.Str(allow_none=True)
    queue = RefOrObject(fields.Str(allow_none=True))
    presets = RefOrObject(fields.List(fields.Str(allow_none=True)))
    cache = fields.Nested(CacheSchema, allow_none=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )
    run_patch = fields.Dict(keys=fields.Str(), values=fields.Raw(), allow_none=True)
    patch_strategy = fields.Str(
        allow_none=True, validate=validate.OneOf(V1PatchStrategy.allowable_values)
    )

    @staticmethod
    def schema_config():
        return V1Build


class V1Build(BaseConfig, polyaxon_sdk.V1Build):
    """You can configure Polyaxon to automatically trigger a build process anytime
    the component or operation is instantiated.

    the build section allows to dynamically recreate a new docker image
    that will be used to run the main logic.
    The new image is generated automatically and automatically set on the main container,
    the name is based on the project name and the run's uuid, i.e. `project:build-uuid`.

    > **Note**: When the build and matrix sections are used together,
    > a single build operation will be scheduled and will be used for all runs.

    > **Note**: When the build section is defined and an upload is triggered,
    > the uploaded artifacts will be pushed to the build run.

    Args:
        hub_ref: str
        connection: str
        queue: str, optional
        presets: List[str], optional
        cache: [V1Cache](/docs/automation/helpers/cache/), optional
        params: Dict[str, [V1Param](/docs/core/specification/params/)], optional
        run_patch: Dict, optional
        patch_strategy: str, optional, defaults to post_merge

    ## YAML usage

    ```yaml
    >>> build:
    >>>   hubRef: kaniko
    >>>   connection: registry-connection-name
    >>>   params:
    >>>     context:
    >>>       value: "path/to/context"
    ```

    ## Python usage

    ```python
    >>> from polyaxon.lifecycle import V1Statuses
    >>> from polyaxon.polyflow import V1Build, V1Param
    >>> build = V1Build(
    >>>     hub_ref="kaniko",
    >>>     connection="registry-connection-name",
    >>>     params={
    >>>         "context": V1Param(value="path/to/context"),
    >>>         ...
    >>>     },
    >>> )
    ```

    ## Fields

    ### hubRef

    Polyaxon provides a [Component Hub](/docs/management/component-hub/)
    for hosting versioned components with an access control system to improve
    the productivity of your team.

    To trigger a build based on a component hosted on Polyaxon Component Hub, you can use `hubRef`

    ```yaml
    >>> build:
    >>>   hubRef: kaniko
    ...
    ```

    Or custom hook component

    ```yaml
    >>> build:
    >>>   hubRef: my-component:dev
    ...
    ```

    ### Connection

    The connection to use for pushing the image. Polyaxon will automatically generate a valid image
    based on the project name and the build operation uuid.

    ```yaml
    >>> build:
    >>>   connection: registry-conneciton-name
    ...
    ```

    ### queue

    The [queue](/docs/core/scheduling-strategies/queues/) to use.
    If not provided, the default queue will be used.

    ```yaml
    >>> build:
    >>>   queue: agent-name/queue-name
    ```

    If the agent name is not specified, Polyaxon will resolve the name of the queue
    based on the default agent.

    ```yaml
    >>> build:
    >>>   queue: queue-name
    ```

    ### presets

    The [presets](/docs/management/organizations/presets/) to use for the hook operation,
    if provided, it will override the component's presets otherwise
    the presets of the component will be used if available.

    ```yaml
    >>> build:
    >>>   presets: [test]
    ```

    ### cache

    The [cache](/docs/automation/helpers/cache/) to use for the build operation,
    if provided, it will override the component's cache otherwise
    the cache of the component will be used if it exists.

    ```yaml
    >>> operation:
    >>>   cache:
    >>>     disable: false
    >>>     ttl: 100
    ```

    ### params

    The [params](/docs/core/specification/params/) to pass if the handler requires extra params,
    they will be validated against the inputs/outputs.
    If a parameter is passed and the component does not define a corresponding inputs/outputs,
    a validation error will be raised unless the param has the `contextOnly` flag enabled.

    ```yaml
    >>> build:
    >>>   params:
    >>>     param1: {value: 1.1}
    >>>     param2: {value: test}
    >>>   ...
    ```

    Params can be used to pass any number of parameters that the component is expecting.

    Example setting the `context`:

    ```yaml
    >>> build:
    >>>   params:
    >>>     context:
    >>>       value: "{{ globals.artifacts_path }}/repo-name"
    ```

    You can use the params field to define your own image destination with either a
    fixed value like `foo/bar:test` or
    templated with the context information:

    ```yaml
    >>> build:
    >>>   params:
    >>>     destination:
    >>>       value: "org/repo:{{ globals.uuid }}"
    ```

    Or provide the connection under the parameter

    ```yaml
    >>> build:
    >>>   params:
    >>>     destination:
    >>>       value: "org/{{ globals.project_name }}:{{ globals.uuid }}"
    >>>       connection: connection-name
    ```

    Polyaxon will use by default the following destination if no destination parameter is provided:
    `{{ globals.project_name }}:{{ globals.uuid }}` and it will use by default the connection
    defined in the build process.

    ### runPatch

    The run patch provides a way to override information about the component's run section,
    for example the container's resources, the environment section, or the init section.

    The run patch is a dictionary that can modify most of the runtime information and
    will be resolved against the corresponding run kind, in this case
    [V1Job](/docs/experimentation/jobs/).

    ### patchStrategy

    Defines how the compiler should handle keys that are defined on the component,
    or how to merge multiple presets when using the override behavior `-f`.

    There are four strategies:
     * `replace`: replaces all keys with new values if provided.
     * `isnull`: only applies new values if the keys have empty/None values.
     * `post_merge`: applies deep merge where newer values are applied last.
     * `pre_merge`: applies deep merge where newer values are applied first.
    """

    IDENTIFIER = "build"
    SCHEMA = BuildSchema
    REDUCED_ATTRIBUTES = [
        "hubRef",
        "connection",
        "queue",
        "presets",
        "cache",
        "params",
        "runPatch",
        "patchStrategy",
    ]
