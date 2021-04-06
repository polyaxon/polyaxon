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

from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow.params import ParamSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class TunerSchema(BaseCamelSchema):
    hub_ref = fields.Str(required=True)
    queue = RefOrObject(fields.Str(allow_none=True))
    presets = RefOrObject(fields.List(fields.Str(allow_none=True)))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )

    @staticmethod
    def schema_config():
        return V1Tuner


class V1Tuner(BaseConfig, polyaxon_sdk.V1Tuner):
    """You can configure Polyaxon to use a custom tuner to customize the built-in optimizers.

    The tuner allows you to customize the behavior of the operations that
    generate new suggestions based on the previous observations.

    You can provide a queue or provide presets to override
    the default configuration of the component.
    You can resolve any context information from the main operation inside a tuner,
    like params, globals, ...

    To override the complete behavior users can provide their own component.

    Args:
        hub_ref: str, optional
        queue: List[str], optional
        presets: List[str], optional
        params: Dict[str, [V1Param](/docs/core/specification/params/)], optional

    ## YAML usage

    ```yaml
    >>> tuner:
    >>>   hubRef: acme/custom-tuner
    ```

    ## Python usage

    ```python
    >>> from polyaxon.lifecycle import V1Statuses
    >>> from polyaxon.polyflow import V1Tuner
    >>> tuner = V1Tuner(
    >>>     hub_ref="acme/custom-tuner",
    >>>     queue="agent-name/queue-name",
    >>>     persets=["preset1", "preset2"],
    >>> )
    ```

    ## Fields

    ### hubRef

    For several algorithms, Polyaxon provides built-in tuners. these tuners
    are hosted on the public component hub. Users can customize or
    build different service to generate new suggestions.

    To provide a custom component hosted on Polyaxon Component Hub, you can use `hubRef`

    ```yaml
    >>> tuner:
    >>>   hubRef: acme/optimizer-logic:v1
    ...
    ```

    ### queue

    The [queue](/docs/core/scheduling-strategies/queue-routing/) to use.
    If not provided, the default queue will be used.

    ```yaml
    >>> tuner:
    >>>   queue: agent-name/queue-name
    ```

    If the agent name is not specified, Polyaxon will resolve the name of the queue
    based on the default agent.

    ```yaml
    >>> hook:
    >>>   queue: queue-name
    ```

    ### presets

    The [presets](/docs/management/organizations/presets/) to use for the tuner operation,
    if provided, it will override the component's presets otherwise
    the presets of the component will be used if available.

    ```yaml
    >>> tuner:
    >>>   presets: [test]
    ```

    ### params

    The [params](/docs/core/specification/params/) to pass if the handler requires extra params,
    they will be validated against the inputs/outputs.
    If a parameter is passed and the component does not define a corresponding inputs/outputs,
    a validation error will be raised unless the param has the `contextOnly` flag enabled.

    ```yaml
    >>> tuner:
    >>>   params:
    >>>     param1: {value: 1.1}
    >>>     param2: {value: test}
    >>>   ...
    ```
    """

    IDENTIFIER = "tuner"
    SCHEMA = TunerSchema
    REDUCED_ATTRIBUTES = [
        "hubRef",
        "params",
        "queue",
        "presets",
    ]
