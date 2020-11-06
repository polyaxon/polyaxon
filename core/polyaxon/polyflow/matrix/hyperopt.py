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
from polyaxon.polyflow.matrix.base import BaseSearchConfig
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.params import HpParamSchema
from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.fields.swagger import SwaggerField


class HyperoptSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1MatrixKind.HYPEROPT))
    max_iterations = RefOrObject(fields.Int(allow_none=True))
    algorithm = fields.Str(
        allow_none=True, validate=validate.OneOf(["tpe", "rand", "anneal"])
    )
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(HpParamSchema), required=True
    )
    num_runs = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    concurrency = fields.Int(allow_none=True)
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": MAIN_JOB_CONTAINER},
        allow_none=True,
    )
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Hyperopt


class V1Hyperopt(BaseSearchConfig, polyaxon_sdk.V1Hyperopt):
    """Hyperopt is a search algorithm that is backed by the
    [Hyperopt](http://hyperopt.github.io/hyperopt/) library
    to perform sequential model-based hyperparameter optimization.

    the Hyperopt integration exposes 3 algorithms: `tpe`, `rand`, `anneal`.

    Args:
        kind: hyperopt
        algorithm: str, one of tpe, rand, anneal
        params: List[Dict[str,
        [params](/docs/automation/optimization-engine/params/#discrete-values)]]
        maxIterations: int, optional
        concurrency: int, optional
        num_runs: int, optional
        seed: int, optional
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional


    ## YAML usage

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   algorithm:
    >>>   maxIterations:
    >>>   concurrency:
    >>>   params:
    >>>   numRuns:
    >>>   seed:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import (
    >>>     V1Hyperopt, V1HpLogSpace, V1HpUniform, V1FailureEarlyStopping, V1MetricEarlyStopping
    >>> )
    >>> matrix = V1Hyperopt(
    >>>   algorithm="tpe",
    >>>   num_runs=20,
    >>>   concurrency=2,
    >>>   seed=23,
    >>>   params={"param1": V1HpLogSpace(...), "param2": V1HpUniform(...), ... },
    >>>   early_stopping=[V1FailureEarlyStopping(...), V1MetricEarlyStopping(...)]
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this matrix is hyperopt.

    If you are using the python client to create the mapping,
    this field is not required and is set by default.

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    ```

    ### algorithm

    The algorithm to use from the hyperopt library, the supported
    algorithms: `tpe`, `rand`, `anneal`.

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   algorithm: anneal
    ```

    ### concurrency

    An optional value to set the number of concurrent operations.

    <blockquote class="light">
    This value only makes sense if less or equal to the total number of possible runs.
    </blockquote>

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
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
    >>>   kind: hyperopt
    >>>   params:
    >>>     param1:
    >>>        kind: ...
    >>>        value: ...
    >>>     param2:
    >>>        kind: ...
    >>>        value: ...
    ```

    ### numRuns

    Maximum number of runs to start based on the search space defined.

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   numRuns: 5
    ```

    ### maxIterations

    Maximum number of iterations to run the process of \\-> suggestions -> training ->\\

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   maxIterations: 5
    ```

    ### seed

    Since this algorithm uses random generators,
    if you want to control the seed for the random generator, you can pass a seed.

     ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   seed: 523
    ```

    ### earlyStopping

    A list of early stopping conditions to check for terminating
    all operations managed by the pipeline.
    If one of the early stopping conditions is met,
    a signal will be sent to terminate all running and pending operations.

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   earlyStopping: ...
    ```

    ### container

    The container with the logic for creating new suggestions based on bayesian optimization,
    users can override this section to provide different resources requirements for the tuner.

    ```yaml
    >>> matrix:
    >>>   kind: hyperopt
    >>>   container: ...
    ```
    """

    SCHEMA = HyperoptSchema
    IDENTIFIER = V1MatrixKind.HYPEROPT
    REDUCED_ATTRIBUTES = [
        "numRuns",
        "seed",
        "concurrency",
        "earlyStopping",
        "container",
    ]

    def create_iteration(self, iteration: int = None) -> int:
        if iteration is None:
            return 0
        return iteration + 1

    def should_reschedule(self, iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        if not self.max_iterations:
            return True
        return iteration < self.max_iterations
