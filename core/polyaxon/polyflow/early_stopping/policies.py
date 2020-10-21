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

from polyaxon.polyflow.optimization import V1Optimization
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig, BaseOneOfSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class MedianStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("median"))
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1MedianStoppingPolicy


class V1MedianStoppingPolicy(BaseConfig, polyaxon_sdk.V1MedianStoppingPolicy):
    IDENTIFIER = "median"
    SCHEMA = MedianStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class TruncationStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("truncation"))
    percent = RefOrObject(fields.Float(), required=True)
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1TruncationStoppingPolicy


class V1TruncationStoppingPolicy(BaseConfig, polyaxon_sdk.V1TruncationStoppingPolicy):
    IDENTIFIER = "truncation"
    SCHEMA = TruncationStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class DiffStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("diff"))
    percent = RefOrObject(fields.Float(), required=True)
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1DiffStoppingPolicy


class V1DiffStoppingPolicy(BaseConfig, polyaxon_sdk.V1DiffStoppingPolicy):
    IDENTIFIER = "diff"
    SCHEMA = DiffStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class StoppingPolicySchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1MedianStoppingPolicy.IDENTIFIER: MedianStoppingPolicySchema,
        V1TruncationStoppingPolicy.IDENTIFIER: TruncationStoppingPolicySchema,
        V1DiffStoppingPolicy.IDENTIFIER: DiffStoppingPolicySchema,
    }


class MetricEarlyStoppingSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("metric_early_stopping"))
    metric = RefOrObject(fields.Str(), required=True)
    value = RefOrObject(fields.Float(), required=True)
    optimization = RefOrObject(
        fields.Str(validate=validate.OneOf(V1Optimization.VALUES)), required=True
    )
    policy = fields.Nested(StoppingPolicySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1MetricEarlyStopping


class V1MetricEarlyStopping(BaseConfig, polyaxon_sdk.V1MetricEarlyStopping):
    """Metric early stopping is an early stopping strategy based on metrics of runs,
    it allows to terminate a dag, a mapping, or hyperparameter tuning when a run's metric(s)
    meet(s) one or multiple conditions.

    If no policy is set and a metric early stopping condition is met the pipeline will be marked
    as succeeded and all pending or running operations will be stopped.

    If a policy is set only the runs that validate the policy will be stopped.

    Args:
        kind: str, should be equal to `metric_early_stopping`
        metric: str
        value: float
        optimization: Union["maximize", "minimize"]
        policy: Union[V1MedianStoppingPolicy,
                V1TruncationStoppingPolicy,
                V1DiffStoppingPolicy], optional

    ## YAML usage

    ```yaml
    >>> earlyStopping:
    >>>   - kind: metric_early_stopping
    >>>     metric: loss
    >>>     value: 0.001
    >>>     optimization: minimize
    >>>   - kind: metric_early_stopping
    >>>     metric: accuaracy
    >>>     value: 0.9
    >>>     optimization: maximize
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1MetricEarlyStopping, V1Optimization
    >>> early_stopping = [
    >>>     V1MetricEarlyStopping(metric="loss", optimization=V1Optimization.MINIMIZE),
    >>>     V1MetricEarlyStopping(metric="accuracy", optimization=V1Optimization.MAXIMIZE),
    >>> ]
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools
    that this early stopping is `metric_early_stopping`.

    If you are using the python client to create the early stopping,
    this field is not required and is set by default.

    ```yaml
    >>> earlyStopping:
    >>>   - kind: metric_early_stopping
    ```

    ### metric

    The metric to track for checking the early stopping condition.
    This metric should be logged using one of the tracking modules or API.

    ```yaml
    >>> earlyStopping:
    >>>   - metric: loss
    ```

    ### value

    The metric value for checking the early stopping condition.

    ```yaml
    >>> earlyStopping:
    >>>   - value: 0.5
    ```

    ### optimization

    The optimization defines the goal or how to measure the performance of the defined metric.

    ```yaml
    >>> earlyStopping:
    >>>   - optimization: maximize
    ```

    ### policy

    A policy allows to defines how to evaluate the metric value against the defined value,
    there are a couple of policies:
     * MedianStopping: Early stopping with median stopping,
         this policy computes running medians across all runs and stops
         those whose best performance is worse than the median of the running runs.
     * DiffStopping: Early stopping with diff factor stopping,
        this policy computes checked runs against the best run and
        stops those whose performance is worse than the best by the factor defined by the user.
     * TruncationStopping: Early stopping with truncation stopping,
        this policy stops a percentage of all running runs at every evaluation.
    """

    SCHEMA = MetricEarlyStoppingSchema
    IDENTIFIER = "metric_early_stopping"


class FailureEarlyStoppingSchema(BaseCamelSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.Equal("failure_early_stopping")
    )
    percent = RefOrObject(fields.Float(), required=True)

    @staticmethod
    def schema_config():
        return V1FailureEarlyStopping


class V1FailureEarlyStopping(BaseConfig, polyaxon_sdk.V1FailureEarlyStopping):
    """Failure early stopping is an early stopping strategy based on statuses of runs that allows
    to terminate a dag, a mapping, or hyperparameter tuning group
    when they reach a certain level of failures.

    If a percentage of the runs in the pipeline fail,
    the pipeline will be marked as failed as well,
    and all pending or running operations will be stopped.

    Args:
        kind: str, should be equal to `failure_early_stopping`
        percent: int (>0, <=99)


    ## YAML usage

    ```yaml
    >>> earlyStopping:
    >>>   - kind: failure_early_stopping
    >>>     percent: 50
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1FailureEarlyStopping
    >>> early_stopping = [V1FailureEarlyStopping(percent=50)]
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools
    that this early stopping is `failure_early_stopping`.

    If you are using the python client to create the early stopping,
    this field is not required and is set by default.

    ```yaml
    >>> earlyStopping:
    >>>   - kind: failure_early_stopping
    ```

    ### percent

    The percentage of failed runs at each evaluation interval,
    should be a value between 1 and 99.

    ```yaml
    >>> earlyStopping:
    >>>   - kind: failure_early_stopping
    >>>     percent: 30
    ```
    """

    IDENTIFIER = "failure_early_stopping"
    SCHEMA = FailureEarlyStoppingSchema
