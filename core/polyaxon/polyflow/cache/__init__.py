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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class CacheSchema(BaseCamelSchema):
    disable = fields.Bool(allow_none=True)
    ttl = fields.Int(allow_none=True)
    inputs = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Cache


class V1Cache(BaseConfig, polyaxon_sdk.V1Cache):
    """Polyaxon provides a caching layer for operation executions,
    this behavior is enabled by default for all runs executed in the context of a DAG,
    a hyperparameter tuning, or a mapping.

    When runs are cached their outputs will be reused for future
    runs with similar inputs and component version.

    Args:
        disable: bool, optional, default: False
        ttl: int, optional
        inputs: List[str], optional

    ## YAML usage

    ```yaml
    >>> cache:
    >>>   disable:
    >>>   ttl:
    >>>   inputs:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Cache
    >>> cache = V1Cache(
    >>>   disable=False,
    >>>   ttl=3600,
    >>>   inputs=['param1', 'param4']
    >>> )
    ```

    ## Fields

    ### disable

    Caching is enabled by default, if you want to disable the cache
    for a component or just for a specific component run, you can set this field to `false`

    ```yaml
    >>> cache:
    >>>   disable: true
    ```

    ### ttl

    the default caching behavior is to persist and reuse a run's results everytime a new operation
    with similar characteristics is scheduled to run.

    In order to invalidate the cache after a certain period of time you can
    define a time to live value.

    ```yaml
    >>> cache:
    >>>   ttl: 36000  # 10 hours
    ```

    ### inputs

    Sometime you might want to discard an input from being considered for
    the cache state calculation,
    or you might want to cache a component's run irrespective of the params you pass to some inputs.

    This field gives you full control to define how you want to calculate the cache state.

    ```yaml
    >>> cache:
    >>>   inputs: ['param1', 'param4']
    ```
    """

    SCHEMA = CacheSchema
    IDENTIFIER = "cache"
    REDUCED_ATTRIBUTES = ["disable", "ttl", "inputs"]
