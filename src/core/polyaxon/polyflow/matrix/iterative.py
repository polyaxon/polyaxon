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

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.matrix.base import BaseSearchConfig
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.params import HpParamSchema
from polyaxon.polyflow.matrix.tuner import TunerSchema
from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class IterativeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1MatrixKind.ITERATIVE))
    max_iterations = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    concurrency = RefOrObject(fields.Int(allow_none=True))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(HpParamSchema), allow_none=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    tuner = fields.Nested(TunerSchema, allow_none=True)
    early_stopping = fields.List(fields.Nested(EarlyStoppingSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Iterative


class V1Iterative(BaseSearchConfig, polyaxon_sdk.V1Iterative):
    """To build a custom optimization algorithm, this interface lets you create an iterative
    process for creating suggestions and training your model based on those suggestions

    The iterative process expect a user defined a tuner that will generate the suggestions for
    running the component.

    Args:
        kind: str, should be equal `iterative`
        max_iterations: int
        params: List[Dict[str, [params](/docs/automation/optimization-engine/params/)]]
        concurrency: int, optional
        seed: int, optional
        tuner: [V1Tuner](/docs/automation/optimization-engine/tuner/), optional
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional

    ## YAML usage

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   concurrency:
    >>>   params:
    >>>   maxIterations:
    >>>   seed:
    >>>   tuner:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.k8s import k8s_schemas
    >>> from polyaxon.polyflow import (
    >>>     V1Iterative,
    >>>     V1HpLogSpace,
    >>>     V1HpUniform,
    >>>     V1FailureEarlyStopping,
    >>>     V1MetricEarlyStopping,
    >>>     V1Tuner,
    >>> )
    >>> matrix = V1Iterative(
    >>>   max_iterations=20,
    >>>   concurrency=2,
    >>>   seed=23,
    >>>   params={"param1": V1HpLogSpace(...), "param2": V1HpUniform(...), ... },
    >>>   early_stopping=[V1FailureEarlyStopping(...), V1MetricEarlyStopping(...)],
    >>>   tuner=V1Tuner(hub_ref="org/my-suggestion-component")
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this matrix is an iterative process.

    If you are using the python client to create the mapping,
    this field is not required and is set by default.

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    ```

    ### concurrency

    An optional value to set the number of concurrent operations.

    <blockquote class="light">
    This value only makes sense if less or equal to the total number of possible runs.
    </blockquote>

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   concurrency: 2
    ```

    For more details about concurrency management,
    please check the [concurrency section](/docs/automation/helpers/concurrency/).

    ### params

    A dictionary of `key -> value generator`
    to generate the parameters.

    To learn about all possible
    [params generators](/docs/automation/optimization-engine/params/).

    > The parameters generated will be validated against
    > the component's inputs/outputs definition to check that the values
    > can be passed and have valid types.

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   params:
    >>>     param1:
    >>>        kind: ...
    >>>        value: ...
    >>>     param2:
    >>>        kind: ...
    >>>        value: ...
    ```

    ### maxIterations

    Maximum number of iterations to run the process of \\-> suggestions -> training ->\\

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   maxIterations: 5
    ```

    ### seed

    Since this algorithm uses random generators,
    if you want to control the seed for the random generator, you can pass a seed.

     ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   seed: 523
    ```

    ### earlyStopping

    A list of early stopping conditions to check for terminating
    all operations managed by the pipeline.
    If one of the early stopping conditions is met,
    a signal will be sent to terminate all running and pending operations.

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   earlyStopping: ...
    ```

    For more details please check the
    [early stopping section](/docs/automation/helpers/early-stopping/).

    ### tuner

    The tuner reference definition (with a component hub reference) to use.
    The component contains the logic for creating new suggestions.

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   tuner:
    >>>     hubRef: acme/suggestion-logic:v1
    ```

    ## Example

    In this example the iterative process will try run 5 iterations generating new experiments
    based on the search space defined in the params subsection.


    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> matrix:
    >>>   kind: iterative
    >>>   concurrency: 10
    >>>   maxIterations: 5
    >>>   tuner:
    >>>     hubRef: my-suggestion-component
    >>>   params:
    >>>     lr:
    >>>       kind: logspace
    >>>       value: 0.01:0.1:5
    >>>     dropout:
    >>>       kind: choice
    >>>       value: [0.2, 0.5]
    >>>    activation:
    >>>       kind: pchoice
    >>>       value: [[elu, 0.1], [relu, 0.2], [sigmoid, 0.7]]
    >>>    early_stopping:
    >>>      - metric: accuracy
    >>>        value: 0.9
    >>>        optimization: maximize
    >>>      - metric: loss
    >>>        value: 0.05
    >>>        optimization: minimize
    >>> component:
    >>>   inputs:
    >>>     - name: batch_size
    >>>       type: int
    >>>       isOptional: true
    >>>       value: 128
    >>>     - name: lr
    >>>       type: float
    >>>     - name: dropout
    >>>       type: float
    >>>     - name: activation
    >>>       type: str
    >>>   container:
    >>>     image: image:latest
    >>>     command: [python3, train.py]
    >>>     args: [
    >>>         "--batch-size={{ batch_size }}",
    >>>         "--lr={{ lr }}",
    >>>         "--dropout={{ dropout }}",
    >>>         "--activation={{ activation }}"
    >>>     ]
    ```
    """

    IDENTIFIER = V1MatrixKind.ITERATIVE
    SCHEMA = IterativeSchema
    REDUCED_ATTRIBUTES = [
        "maxIterations",
        "params",
        "seed",
        "tuner",
        "earlyStopping",
        "concurrency",
    ]

    def create_iteration(self, iteration: int = None) -> int:
        if iteration is None:
            return 0
        return iteration + 1

    def should_reschedule(self, iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        return iteration < self.max_iterations
