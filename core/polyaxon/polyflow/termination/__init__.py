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


class TerminationSchema(BaseCamelSchema):
    max_retries = fields.Int(allow_none=True)
    ttl = fields.Int(allow_none=True)
    timeout = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return V1Termination


class V1Termination(BaseConfig, polyaxon_sdk.V1Termination):
    """The termination section allows to define and control when
    to stop an operation and how long to keep its resources on the cluster.

    Args:
        max_retries: int, optional
        ttl: int, optional
        timeout: int, optional

    ## YAML usage

    ```yaml
    >>> termination:
    >>>   maxRetries:
    >>>   ttl:
    >>>   timeout:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Termination
    >>> termination = V1Termination(
    >>>     max_retries=1,
    >>>     ttl=1000,
    >>>     timeout=50
    >>> )
    ```

    ## Fields

    ### maxRetries

    Maximum number of retries when an operation fails.

    This field can be used with
    [restartPolicy](/docs/core/specification/environment/#restartpolicy)
    from the environment section.

    This field is the equivalent of the
    [backoffLimit](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/).
    Polyaxon exposes a uniform specification and knows how
    to manage and inject this value into the underlying primitive of the runtime,
    i.e. Job, Service, TFJob CRD, Spark Application CRD, ...

    ```yaml
    >>> termination:
    >>>   maxRetries: 3
    ```

    ### ttl

    Polyaxon will automatically clean all resources just after they finish and after
    the various helpers finish collecting and archiving information from the cluster,
    such as logs, outputs, ... This ensures that your cluster(s) are kept clean and no resources
    are actively putting pressure on the API server.

    That being said, sometimes users might want to keep the resources after
    they finish for sanity check or debugging.

    The ttl field allows you to leverage the TTL controller provided by some primitives,
    for example the
    [ttlSecondsAfterFinished](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#clean-up-finished-jobs-automatically), # noqa
    from the Job controller.
    Polyaxon has helpers for resources that don't have a built-in TTL mechanism, such as services,
    so that you can have a uniform definition for all of your operations.

    ```yaml
    >>> termination:
    >>>   ttl: 1000
    ```


    ### timeout

    Sometime you might to stop an operation after a certain time, timeout let's you define how
    long before Polyaxon decides to stop that operation, this is the equivalent of Kubernetes Jobs
    [activeDeadlineSeconds](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#job-termination-and-cleanup)  # noqa
    but you can use this field for all runtimes, for instance you might want to stop a
    tensorboard after 12 hours, this way you don't have to actively look for running tensorboards.

    ```yaml
    >>> termination:
    >>>   timeout: 1000
    ```
    """

    IDENTIFIER = "termination"
    SCHEMA = TerminationSchema
    REDUCED_ATTRIBUTES = ["maxRetries", "timeout", "ttl"]
