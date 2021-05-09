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
import math

from typing import Tuple

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.matrix.base import BaseSearchConfig
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.params import HpParamSchema
from polyaxon.polyflow.matrix.tuner import TunerSchema
from polyaxon.polyflow.optimization import (
    OptimizationMetricSchema,
    OptimizationResourceSchema,
)
from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class HyperbandSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1MatrixKind.HYPERBAND))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(HpParamSchema), allow_none=True
    )
    max_iterations = RefOrObject(fields.Int(validate=validate.Range(min=1)))
    eta = RefOrObject(fields.Float(validate=validate.Range(min=0)))
    resource = fields.Nested(OptimizationResourceSchema)
    metric = fields.Nested(OptimizationMetricSchema)
    resume = RefOrObject(fields.Boolean(allow_none=True))
    seed = RefOrObject(fields.Int(allow_none=True))
    concurrency = RefOrObject(fields.Int(allow_none=True))
    tuner = fields.Nested(TunerSchema, allow_none=True)
    early_stopping = fields.List(fields.Nested(EarlyStoppingSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Hyperband


class V1Hyperband(BaseSearchConfig, polyaxon_sdk.V1Hyperband):
    """Hyperband is a relatively new method for tuning iterative algorithms.
    It performs random sampling and attempts to gain an edge
    by using time spent optimizing in the best way.

    The algorithm tries a large number of random configurations/experiments,
    then decides which configurations to keep based on their progress.

    The way Hyperband is implemented, it creates several buckets,
    each bucket has a number of randomly generated hyperparameter configurations,
    each configuration uses a resource (e.g. number of steps, number of epochs, batch size, ...).

    To adapt the algorithm's maximum resource allocation, users can use `maxIterations`.

    After trying a number of configurations, it chooses the top `number of observation/eta`
    configurations and runs them using an increased `resource*eta` resource.
    At last, it chooses the best configuration it has found so far.

    The way Hyperband works is by discarding poor performing
    configurations leaving more resources for more promising configurations
    during the successive halving.

    In order to use Hyperband correctly, you must define a metric called
    `resource` that the algorithm will increase iteratively.

    Args:
        kind: string, should be equal to `hyperband`
        params: List[Dict[str, [params](/docs/automation/optimization-engine/params/#discrete-values)]]  # noqa
        max_iterations: int
        eta: int
        resource: V1OptimizationResource
        metric: V1OptimizationMetric
        resume: bool, optional
        seed: int, optional
        concurrency: int, optional
        tuner: [V1Tuner](/docs/automation/optimization-engine/tuner/), optional
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional

    ## YAML usage

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   concurrency:
    >>>   maxIterations:
    >>>   resource:
    >>>   metric:
    >>>   resume:
    >>>   params:
    >>>   seed:
    >>>   tuner:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.polyflow import (
    >>>     V1Hyperband, V1HpLogSpace, V1HpChoice, V1FailureEarlyStopping, V1MetricEarlyStopping,
    >>>     V1OptimizationMetric, V1Optimization, V1OptimizationResource,
    >>> )
    >>> matrix = V1Hyperband(
    >>>   concurrency=20,
    >>>   params={"param1": V1HpLogSpace(...), "param2": V1HpChoice(...), ... },
    >>>   resume=True,
    >>>   metric=V1OptimizationMetric(name="loss", optimization=V1Optimization.MINIMIZE),
    >>>   resource=V1OptimizationResource(name="num_steps", type=types.INT),
    >>>   early_stopping=[V1FailureEarlyStopping(...), V1MetricEarlyStopping(...)]
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this matrix is hyperband.

    If you are using the python client to create the mapping,
    this field is not required and is set by default.

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    ```

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
    >>>   kind: hyperband
    >>>   params:
    >>>     param1:
    >>>        kind: ...
    >>>        value: ...
    >>>     param2:
    >>>        kind: ...
    >>>        value: ...
    ```

    ### maxIterations

    The algorithm's maximum resource allocation.

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   maxIterations: 81
    ```

    ### eta

    A parameter that tunes:
     * The downsampling factor: `number of observation/eta`
     * The resource increase factor: `resource*eta`

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   eta: 3
    ```

    ### resource

    The resource to optimize (should be an int or a float),
    the resource van be the number of steps or epochs,

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   resource:
    >>>     name: num_steps
    >>>     type: int
    ```

    ### metric

    The metric to optimize during the iterations,
    this is the metric that you want to maximize or minimize.

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   metric:
    >>>     name: loss
    >>>     optimization: minimize
    ```

    ### resume

    A flag to resume or restart the selected runs, default to false (restart)

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   resume: True
    ```

    ### concurrency

    An optional value to set the number of concurrent operations.

    <blockquote class="light">
    This value only makes sense if less or equal to the total number of possible runs.
    </blockquote>

    ```yaml
    >>> matrix:
    >>>   kind: random
    >>>   concurrency: 2
    ```

    For more details about concurrency management,
    please check the [concurrency section](/docs/automation/helpers/concurrency/).

    ### seed

    Since this algorithm uses random generators,
    if you want to control the seed for the random generator, you can pass a seed.

     ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   seed: 523
    ```

    ### earlyStopping

    A list of early stopping conditions to check for terminating
    all operations managed by the pipeline.
    If one of the early stopping conditions is met,
    a signal will be sent to terminate all running and pending operations.

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   earlyStopping: ...
    ```

    For more details please check the
    [early stopping section](/docs/automation/helpers/early-stopping/).

    ### tuner

    The tuner reference (w/o a component hub reference) to use.
    The component contains the logic for creating new suggestions,
    users can override this section to provide a different tuner component.

    ```yaml
    >>> matrix:
    >>>   kind: hyperband
    >>>   tuner:
    >>>     hubRef: 'acme/my-hyperband-tuner:version'
    ```

    ## Example

    This is an example of using hyperband for hyperparameter search:

    ```yaml
    >>> version: 1.1
    >>> kind: operation
    >>> matrix:
    >>>   kind: hyperband
    >>>   concurrency: 5
    >>>   maxIterations: 81
    >>>   eta: 3
    >>>   resource:
    >>>     name: num_steps
    >>>     type: int
    >>>   metric:
    >>>     name: loss
    >>>     optimization: minimize
    >>>   resume: False
    >>>   params:
    >>>     lr:
    >>>       kind: uniform
    >>>       value: [0, 0.9]
    >>>     dropout:
    >>>       kind: choice
    >>>       value: [0.25, 0.3]
    >>>     activation:
    >>>       kind: pchoice
    >>>       value: [[relu, 0.1], [sigmoid, 0.8]]
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
    >>>     - name: logspace
    >>>       type: float
    >>>     - name: dropout
    >>>       type: float
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

    In this example we allocate a maximum resources of `81`,
    our resource in this case is the `num_steps` which is of type `int` that we pass to our model.

    This is how the algorithm works with this config:

    |              | bucket=4   |                | bucket=3   |                 | bucket=2    |                | bucket=1   |                 | bucket=0   |                | # noqa
    |--------------|------------|----------------|------------|-----------------|-------------|----------------|------------|-----------------|------------|----------------| # noqa
    |iteration     |num configs |resource alloc  |num configs |resource alloc   |num configs  |resource alloc  |num configs |resource alloc   |num configs |resource alloc  | # noqa
    |0             |81          |1               |27          |3                |9            |9               |6           |27               |5           |             81 | # noqa
    |1             |27          |3               |9           |9                |3            |27              |2           |81               |            |                | # noqa
    |2             |9           |9               |3           |27               |1            |81              |            |                 |            |                | # noqa
    |3             |3           |27              |1           |81               |             |                |            |                 |            |                | # noqa
    |4             |1           |81              |            |                 |             |                |            |                 |            |                | # noqa
    """

    SCHEMA = HyperbandSchema
    IDENTIFIER = V1MatrixKind.HYPERBAND
    REDUCED_ATTRIBUTES = ["seed", "concurrency", "earlyStopping", "tuner"]

    def set_tuning_params(self):
        # Maximum iterations per configuration: max_iterations
        # Defines configuration downsampling/elimination rate (default = 3): eta
        # number of times to run hyperband (brackets)
        # i.e.  # of times to repeat the outer loops over the tradeoffs `s`
        self.s_max = int(math.log(self.max_iterations) / math.log(self.eta))
        self.B = (
            self.s_max + 1
        ) * self.max_iterations  # budget per bracket of successive halving

    def get_bracket(self, iteration):
        """This defines the bracket `s` in outerloop `for s in reversed(range(self.s_max))`."""
        return self.s_max - iteration

    def should_create_iteration(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration < bracket:
            # The bracket is still processing
            return False

        # We can only reschedule if we can create a new bracket
        return self.get_bracket(iteration=iteration + 1) >= 0

    def get_num_runs_to_keep(self, num_runs, bracket_iteration):
        """Return the number of configs to keep and resume."""
        num_runs = num_runs * (self.eta ** -bracket_iteration)
        return int(num_runs / self.eta)

    def get_num_runs(self, bracket):
        # n: initial number of configs
        return int(
            math.ceil(
                (self.B / self.max_iterations) * (self.eta ** bracket) / (bracket + 1)
            )
        )

    def get_num_runs_to_keep_for_iteration(self, iteration, bracket_iteration):
        """Return the number of configs to keep for an iteration and iteration bracket.

        This is just util function around `get_num_runs_to_keep`
        """
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration == bracket + 1:
            # End of loop `for bracket_iteration in range(bracket + 1):`
            return 0

        num_runs = self.get_num_runs(bracket=bracket)
        return self.get_num_runs_to_keep(
            num_runs=num_runs, bracket_iteration=bracket_iteration
        )

    def should_reduce_configs(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another bracket iteration."""
        num_runs_to_keep = self.get_num_runs_to_keep_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        )
        return num_runs_to_keep > 0

    def create_iteration(
        self, iteration: int = None, bracket_iteration: int = 0
    ) -> Tuple[int, int]:
        """Create an iteration for hyperband."""
        if iteration is None:
            return 0, 0

        should_create_iteration = self.should_create_iteration(
            iteration=iteration,
            bracket_iteration=bracket_iteration,
        )
        should_reduce_configs = self.should_reduce_configs(
            iteration=iteration,
            bracket_iteration=bracket_iteration,
        )
        if should_create_iteration:
            iteration = iteration + 1
            bracket_iteration = 0
        elif should_reduce_configs:
            bracket_iteration = bracket_iteration + 1
        else:
            raise ValueError(
                "Hyperband create iteration failed, "
                "could not reschedule or reduce configs"
            )

        return iteration, bracket_iteration

    def should_reschedule(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        return self.should_create_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        ) or self.should_reduce_configs(
            iteration=iteration,
            bracket_iteration=bracket_iteration,
        )
