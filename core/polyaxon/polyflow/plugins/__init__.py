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

from polyaxon.polyflow.notifications import NotificationSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class PluginsSchema(BaseCamelSchema):
    auth = fields.Bool(allow_none=True)
    docker = fields.Bool(allow_none=True)
    shm = fields.Bool(allow_none=True)
    collect_artifacts = fields.Bool(allow_none=True)
    collect_logs = fields.Bool(allow_none=True)
    collect_resources = fields.Bool(allow_none=True)
    sync_statuses = fields.Bool(allow_none=True)
    log_level = fields.Str(allow_none=True)
    notifications = fields.List(fields.Nested(NotificationSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Plugins


class V1Plugins(BaseConfig, polyaxon_sdk.V1Plugins):
    """Plugins provide a way to set notifications and customize extract Polyaxon utilities.

    By default Polyaxon injects some information for example an auth context
    and triggers some mechanisms for collecting logs and outputs.

    Plugins section exposes more control to the end user to enable/disable some of these utilities.

    Args:
        auth: bool, optional, default: True
        docker: bool, optional, default: False
        shm: bool, optional, default: True
        collect_artifacts: bool, optional, default: True
        collect_logs: bool, optional, default: True
        collect_resources: bool, optional, default: True
        sync_statuses: bool, optional, default: True
        log_level: str, optional
        notifications: List[[V1Notification](/docs/core/specification/notifications/)]

    ## Yaml usage

    ```yaml
    >>> plugins:
    >>>   auth:
    >>>   docker:
    >>>   shm:
    >>>   collectArtifacts:
    >>>   collectLogs:
    >>>   collectResources:
    >>>   syncStatuses:
    >>>   logLevel:
    >>>   notifications:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Plugins
    >>> plugins = V1Plugins(
    >>>     auth=False,
    >>>     docker=True,
    >>>     shm=True.
    >>>     collect_artifacts=False,
    >>>     collect_logs=False,
    >>>     collect_resources=False
    >>>     sync_statuses=False,
    >>>     log_level="INFO",
    >>>     notifications=[V1Notification(...)]
    >>> )
    ```

    ## Fields

    ### auth

    This plugin is enabled by default.

    By default Polyaxon will create an auth context for each operation, this removes the overhead
    to think about how you can pass tokens to your runs,
    or the need to create secrets to load the token from during the run time.

    The auth context that Polyaxon provides is not only specific to the user who
    executed the run, but also it impersonates similar access rights, it has the same scopes
    and restrictions the user usually has within the context of the project
    the run is running inside.
    this is important to verify accessed resources and APIs calls initiated during the run
    by the user's code.

    Oftentimes, users might not need to use an authenticated client inside their containers,
    in that case they can disable this plugin.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   auth: false
    ```

    ### docker

    This plugin is disabled by default.

    This plugin allows to expose docker docket volume to your runs.

    N.B. use this plugin carefully, you might also need to check with your devops
    team before using it, it requires docker.sock of the host to be mounted
    which is often rejected by OPA.

    To enable this plugin:

    ```yaml
    >>> plugins:
    >>>   docker: true
    ```

    ### shm

    This plugin is enabled by default.

    This plugin mounts an tmpfs volume to /dev/shm.
    This will set /dev/shm size to half of the RAM of node.
    By default, /dev/shm is very small, only 64MB.
    Some experiments/jobs will fail due to lack of share memory,
    such as some experiments running on Pytorch.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   shm: false
    ```

    ### collectArtifacts

    This plugin is enabled by default.

    By default Polyaxon will collect all artifacts and outputs that you share in the
    `plx-context/artifacts/run-uuid/outputs` to the default artifacts store
    that you configured during the deployment.

    This plugin is important if you want to have an agnostic code to the
    type of storage backend your are using, by changing the environment variable
    you can test your code with `tmp` file locally and the artifacts path in production.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   collectArtifacts: false
    ```

    Sometimes you might want to access the artifacts path in your polyaxonfile,
    Polyaxon expose a context that get resolved during the compilation time,
    you can just use "{{artifacts_path}}" global variable and it will be resolved automatically.

    Example:

    ```
    >>> run:
    >>>   kind: job
    >>>   container:
    >>>     command: "cp /some/know/path/file {{artifacts_path}}/file"

    ```

    For more information about the context, please check [context](/docs/core/specification/context/)

    ### collectLogs

    This plugin is enabled by default.

    By default Polyaxon will collect all logs related to you runs before deleting
    the resource on the clusters. This ensures that your cluster(s) are kept clean and no resources
    are actively putting pressure on the API server.

    Sometimes you might want to avoid collecting logs for some runs, for example test or debug jobs.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   collectLogs: false
    ```

    ### collectResources

    This plugin is enabled by default.

    By default Polyaxon will collect all Mem/CPU/GPU resources
    for your runs that use the python client.

    Sometimes you might want to avoid collecting this information for some runs,
    for example test or debug jobs.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   collectResources: false
    ```

    ### syncStatuses

    This plugin is enabled by default.

    Every job that is scheduled on Kubernetes by Polyaxon will be tracked to notify the user about
    it's progress and in case of warnings.

    You will most probably never have to disable this plugin.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   syncStatuses: false
    ```

    ### logLevel

    Default is None.

    If you want to control the log level of your runs in similar way locally and on cluster,
    you can either use env vars or this plugin to share the same log level with all containers
    running in your operation.

    ```yaml
    >>> plugins:
    >>>   logLevel: warning
    ```

    ### notifications

    Default is None.

    This plugin was asked by several users, because Polyaxon used to only expose a global way
    for sending notifications about runs.

    This plugin allows you to enable per run notification configuration.

    For more information about notifications please check the
    [notifications section](/docs/core/specification/notifications/)

    ```yaml
    >>> plugins:
    >>>   notifications:
    >>>     - connections: [slack-connection]
    >>>       trigger: succeeded
    >>>     - connections: [slack-connection, pagerduty-connection]
    >>>       trigger:failed
    ```
    """

    IDENTIFIER = "plugins"
    SCHEMA = PluginsSchema
    REDUCED_ATTRIBUTES = [
        "auth",
        "docker",
        "shm",
        "collectArtifacts",
        "collectLogs",
        "collectResources",
        "syncStatuses",
        "logLevel",
        "notifications",
    ]
