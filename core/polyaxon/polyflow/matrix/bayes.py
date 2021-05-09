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

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.matrix.base import BaseSearchConfig
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.params import HpParamSchema
from polyaxon.polyflow.matrix.tuner import TunerSchema
from polyaxon.polyflow.optimization import OptimizationMetricSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.utils.signal_decorators import check_partial


class AcquisitionFunctions:
    UCB = "ucb"
    EI = "ei"
    POI = "poi"

    UCB_VALUES = [UCB, UCB.upper(), UCB.capitalize()]
    EI_VALUES = [EI, EI.upper(), EI.capitalize()]
    POI_VALUES = [POI, POI.upper(), POI.capitalize()]

    VALUES = UCB_VALUES + EI_VALUES + POI_VALUES

    @classmethod
    def is_ucb(cls, value):
        return value in cls.UCB_VALUES

    @classmethod
    def is_ei(cls, value):
        return value in cls.EI_VALUES

    @classmethod
    def is_poi(cls, value):
        return value in cls.POI_VALUES


class GaussianProcessesKernels:
    RBF = "rbf"
    MATERN = "matern"

    RBF_VALUES = [RBF, RBF.upper(), RBF.capitalize()]
    MATERN_VALUES = [MATERN, MATERN.upper(), MATERN.capitalize()]

    VALUES = RBF_VALUES + MATERN_VALUES

    @classmethod
    def is_rbf(cls, value):
        return value in cls.RBF_VALUES

    @classmethod
    def is_mattern(cls, value):
        return value in cls.MATERN_VALUES


class GaussianProcessSchema(BaseCamelSchema):
    kernel = fields.Str(
        allow_none=True, validate=validate.OneOf(GaussianProcessesKernels.VALUES)
    )
    length_scale = fields.Float(allow_none=True)
    nu = fields.Float(allow_none=True)
    num_restarts_optimizer = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return GaussianProcessConfig


class GaussianProcessConfig(BaseConfig):
    SCHEMA = GaussianProcessSchema
    IDENTIFIER = "gaussian_process"

    def __init__(
        self,
        kernel=GaussianProcessesKernels.MATERN,
        length_scale=1.0,
        nu=1.5,
        num_restarts_optimizer=0,
    ):
        self.kernel = kernel
        self.length_scale = length_scale
        self.nu = nu
        self.num_restarts_optimizer = num_restarts_optimizer


def validate_utility_function(acquisition_function, kappa, eps):
    condition = AcquisitionFunctions.is_ucb(acquisition_function) and kappa is None
    if condition:
        raise ValidationError(
            "the acquisition function `ucb` requires a parameter `kappa`"
        )

    condition = (
        AcquisitionFunctions.is_ei(acquisition_function)
        or AcquisitionFunctions.is_poi(acquisition_function)
    ) and eps is None
    if condition:
        raise ValidationError(
            "the acquisition function `{}` requires a parameter `eps`".format(
                acquisition_function
            )
        )


class UtilityFunctionSchema(BaseCamelSchema):
    acquisition_function = fields.Str(
        allow_none=True, validate=validate.OneOf(AcquisitionFunctions.VALUES)
    )
    gaussian_process = fields.Nested(GaussianProcessSchema, allow_none=True)
    kappa = fields.Float(allow_none=True)
    eps = fields.Float(allow_none=True)
    num_warmup = fields.Int(allow_none=True)
    num_iterations = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return UtilityFunctionConfig

    @validates_schema
    @check_partial
    def validate_utility_function(self, data, **kwargs):
        validate_utility_function(
            acquisition_function=data.get("acquisition_function"),
            kappa=data.get("kappa"),
            eps=data.get("eps"),
        )


class UtilityFunctionConfig(BaseConfig):
    SCHEMA = UtilityFunctionSchema
    IDENTIFIER = "utility_function"
    REDUCED_ATTRIBUTES = ["numWarmup", "numIterations"]

    def __init__(
        self,
        acquisition_function=AcquisitionFunctions.UCB,
        gaussian_process=None,
        kappa=None,
        eps=None,
        num_warmup=None,
        num_iterations=None,
    ):
        validate_utility_function(
            acquisition_function=acquisition_function, kappa=kappa, eps=eps
        )

        self.acquisition_function = acquisition_function
        self.gaussian_process = gaussian_process
        self.kappa = kappa
        self.eps = eps
        self.num_warmup = num_warmup
        self.num_iterations = num_iterations


def validate_matrix(matrix):
    if not matrix:
        return None

    for key, value in matrix.items():
        if value.is_distribution and not value.is_uniform:
            raise ValidationError(
                "`{}` defines a non uniform distribution, "
                "and it cannot be used with bayesian optimization.".format(key)
            )

    return matrix


class BayesSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1MatrixKind.BAYES))
    utility_function = fields.Nested(UtilityFunctionSchema, allow_none=True)
    num_initial_runs = RefOrObject(fields.Int(), required=True)
    max_iterations = RefOrObject(fields.Int(validate=validate.Range(min=1)))
    metric = fields.Nested(OptimizationMetricSchema, required=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(HpParamSchema), required=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    concurrency = RefOrObject(fields.Int(allow_none=True))
    tuner = fields.Nested(TunerSchema, allow_none=True)
    early_stopping = fields.List(fields.Nested(EarlyStoppingSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Bayes

    @validates_schema
    @check_partial
    def validate_matrix(self, data, **kwargs):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get("params"))


class V1Bayes(BaseSearchConfig, polyaxon_sdk.V1Bayes):
    """Bayesian optimization is an extremely powerful technique.
    The main idea behind it is to compute a posterior distribution
    over the objective function based on the data, and then select good points
    to try with respect to this distribution.

    The way Polyaxon performs bayesian optimization is by measuring
    the expected increase in the maximum objective value seen over all
    experiments in the group, given the next point we pick.

    Args:
        kind: string, should be equal to `bayes`
        utility_function: UtilityFunctionConfig
        num_initial_runs: int
        max_iterations: int
        metric: V1OptimizationMetric
        params: List[Dict[str, [params](/docs/automation/optimization-engine/params/#discrete-values)]]  # noqa
        seed: int, optional
        concurrency: int, optional
        tuner: [V1Tuner](/docs/automation/optimization-engine/tuner/), optional
        early_stopping: List[[EarlyStopping](/docs/automation/helpers/early-stopping)], optional


    ## YAML usage

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   utilityFunction:
    >>>   numInitialRuns:
    >>>   maxIterations:
    >>>   metric:
    >>>   params:
    >>>   seed:
    >>>   concurrency:
    >>>   tuner:
    >>>   earlyStopping:
    ```

    ## Python usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.polyflow import (
    >>>     V1Bayes, V1HpLogSpace, V1HpChoice, V1FailureEarlyStopping, V1MetricEarlyStopping,
    >>>     V1OptimizationMetric, V1Optimization, V1OptimizationResource, UtilityFunctionConfig
    >>> )
    >>> matrix = V1Bayes(
    >>>   concurrency=20,
    >>>   utility_function=UtilityFunctionConfig(...),
    >>>   num_initial_runs=40,
    >>>   max_iterations=20,
    >>>   params={"param1": V1HpLogSpace(...), "param2": V1HpChoice(...), ... },
    >>>   metric=V1OptimizationMetric(name="loss", optimization=V1Optimization.MINIMIZE),
    >>>   early_stopping=[V1FailureEarlyStopping(...), V1MetricEarlyStopping(...)]
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this matrix is bayes.

    If you are using the python client to create the mapping,
    this field is not required and is set by default.

    ```yaml
    >>> matrix:
    >>>   kind: bayes
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
    >>>   kind: bayes
    >>>   params:
    >>>     param1:
    >>>        kind: ...
    >>>        value: ...
    >>>     param2:
    >>>        kind: ...
    >>>        value: ...
    ```

    ### utilityFunction

    the utility function defines what acquisition function and bayesian process to use.

    ### Acquisition functions

    A couple of acquisition functions can be used: `ucb`, `ei` or `poi`.

     * `ucb`: Upper Confidence Bound,
     * `ei`: Expected Improvement
     * `poi`: Probability of Improvement

    When using `ucb` as acquisition function, a tunable parameter `kappa`
    is also required, to balance exploitation against exploration, increasing kappa
    will make the optimized hyperparameters pursuing exploration.

    When using `ei` or `poi` as acquisition function, a tunable parameter `eps` is also required,
    to balance exploitation against exploration, increasing epsilon will
    make the optimized hyperparameters more spread out across the whole range.

    ### Gaussian process

    Polyaxon allows to tune the gaussian process.

     * `kernel`: `matern` or `rbf`.
     * `lengthScale`: float
     * `nu`: float
     * `numRestartsOptimizer`: int

     ```yaml
     >>> matrix:
     >>>   kind: bayes
     >>>   utility_function:
     >>>     acquisitionFunction: ucb
     >>>     kappa: 1.2
     >>>     gaussianProcess:
     >>>       kernel: matern
     >>>       lengthScale: 1.0
     >>>       nu: 1.9
     >>>       numRestartsOptimizer: 0
     ```

    ### numInitialRuns

    the initial iteration of random experiments is required to create a seed of observations.

    This initial random results are used by the algorithm to update
    the regression model for generating the next suggestions.

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   numInitialRuns: 40
    ```

    ### maxIterations

    After creating the first set of random observations,
    the algorithm will use these results to update
    the regression model and suggest a new experiment to run.

    Every time an experiment is done,
    the results are used as an observation and are appended
    to the historical values so that the algorithm can use all
    the observations again to suggest more experiments to run.

    The algorithm will keep suggesting more experiments and adding
    their results as an observation, every time we make a new observation,
    i.e. an experiment finishes and reports the results to the platform,
    the results are appended to the historical values, and then used to make a better suggestion.

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   maxIterations: 15
    ```

    This configuration will make 15 suggestions based on the historical values,
    every time an observation is made is appended to the historical values
    to make better subsequent suggestions.

    ### metric

    The metric to optimize during the iterations,
    this is the metric that you want to maximize or minimize.

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   metric:
    >>>     name: loss
    >>>     optimization: minimize
    ```

    ### seed

    Since this algorithm uses random generators,
    if you want to control the seed for the random generator, you can pass a seed.

     ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   seed: 523
    ```

    ### concurrency

    An optional value to set the number of concurrent operations.

    <blockquote class="light">
    This value only makes sense if less or equal to the total number of possible runs.
    </blockquote>

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   concurrency: 20
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
    >>>   kind: bayes
    >>>   earlyStopping: ...
    ```

    For more details please check the
    [early stopping section](/docs/automation/helpers/early-stopping/).

    ### tuner

    The tuner reference (w/o component hub reference) to use.
    The component contains the logic for creating new suggestions based on bayesian optimization,
    users can override this section to provide a different tuner component.

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   tuner:
    >>>     hubRef: 'acme/my-bo-tuner:version'
    ```

    ## Example

    This is an example of using bayesian search for hyperparameter tuning:

    ```yaml
    >>> matrix:
    >>>   kind: bayes
    >>>   concurrency: 5
    >>>   maxIterations: 15
    >>>   numInitialTrials: 30
    >>>   metric:
    >>>     name: loss
    >>>     optimization: minimize
    >>>   utilityFunction:
    >>>     acquisitionFunction: ucb
    >>>     kappa: 1.2
    >>>     gaussianProcess:
    >>>       kernel: matern
    >>>       lengthScale: 1.0
    >>>       nu: 1.9
    >>>       numRestartsOptimizer: 0
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
    >>>   container:
    >>>     image: image:latest
    >>>     command: [python3, train.py]
    >>>     args: [
    >>>         "--batch-size={{ batch_size }}",
    >>>         "--lr={{ lr }}",
    >>>         "--dropout={{ dropout }}",
    >>>         "--activation={{ activation }}"
    ```
    """

    SCHEMA = BayesSchema
    IDENTIFIER = V1MatrixKind.BAYES
    REDUCED_ATTRIBUTES = ["seed", "concurrency", "earlyStopping", "tuner"]

    def create_iteration(self, iteration: int = None) -> int:
        if iteration is None:
            return 0
        return iteration + 1

    def should_reschedule(self, iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        return iteration < self.max_iterations
