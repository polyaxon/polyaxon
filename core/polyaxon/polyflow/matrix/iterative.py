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

from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.params import MatrixSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.fields.swagger import SwaggerField


class IterativeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1MatrixKind.ITERATIVE))
    num_iterations = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    concurrency = fields.Int(allow_none=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": MAIN_JOB_CONTAINER},
        allow_none=True,
    )
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Iterative


class V1Iterative(BaseConfig, polyaxon_sdk.V1Iterative):
    """To build a custom optimization algorithm, this interface lets you create an iterative
    process for creating suggestions and training your model based on those suggestions

    The iterative process expect a user defined container that will generate the suggestions for
    running the component.

    Args:
        kind: str, should be equal `iterative`
        num_iterations: int
        params: List[Dict[str,
        [params](/docs/automation/optimization-engine/params/)]]
        concurrency: int, optional
        seed: int, optional
        container: [Kubernetes Container](https://kubernetes.io/docs/concepts/containers/)
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional

    ## YAML usage

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   concurrency:
    >>>   params:
    >>>   numIterations:
    >>>   seed:
    >>>   container:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.k8s import k8s_schemas
    >>> from polyaxon.polyflow import (
    >>>     V1Iterative, V1HpLogSpace, V1HpUniform, V1FailureEarlyStopping, V1MetricEarlyStopping
    >>> )
    >>> matrix = V1Iterative(
    >>>   num_iterations=20,
    >>>   concurrency=2,
    >>>   seed=23,
    >>>   params={"param1": V1HpLogSpace(...), "param2": V1HpUniform(...), ... },
    >>>   early_stopping=[V1FailureEarlyStopping(...), V1MetricEarlyStopping(...)],
    >>>   container=k8s_schemas.V1Container(name="my-suggestion-container", ...)
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
    the component's inputs/outputs definition to check that the values
    can be passed and have valid types.

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

    ### numIterations

    Maximum number of iterations to run the process of \\-> suggestions -> training ->\\

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   numIterations: 5
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

    ### container

    The container will container the logic for creating new suggestions
    to run the main container in the compoent with different new params combinations.

    ```yaml
    >>> matrix:
    >>>   kind: iterative
    >>>   container: ...
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
    >>>   numIterations: 5
    >>>   container:
    >>>     name: my-suggestion-logic
    >>>     commmand: ...
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
    REDUCED_ATTRIBUTES = ["params", "seed", "container", "earlyStopping", "concurrency"]
