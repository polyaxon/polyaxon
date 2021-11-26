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

from marshmallow import fields

from polyaxon.auxiliaries.sidecar import PolyaxonSidecarContainerSchema
from polyaxon.polyflow.notifications import NotificationSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class PluginsSchema(BaseCamelSchema):
    auth = fields.Bool(allow_none=True)
    docker = fields.Bool(allow_none=True)
    shm = fields.Bool(allow_none=True)
    mount_artifacts_store = fields.Bool(allow_none=True)
    collect_artifacts = fields.Bool(allow_none=True)
    collect_logs = fields.Bool(allow_none=True)
    collect_resources = fields.Bool(allow_none=True)
    sync_statuses = fields.Bool(allow_none=True)
    auto_resume = fields.Bool(allow_none=True)
    external_host = fields.Bool(allow_none=True)
    log_level = fields.Str(allow_none=True)
    notifications = fields.List(fields.Nested(NotificationSchema), allow_none=True)
    sidecar = fields.Nested(
        PolyaxonSidecarContainerSchema,
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return V1Plugins


class V1Plugins(BaseConfig, polyaxon_sdk.V1Plugins):
    """Plugins section provides a way to customize extra Polyaxon utilities.

    By default, Polyaxon injects some information for example an auth context
    and triggers some mechanisms for collecting logs and outputs.

    Plugins section provides more control to the end user to enable/disable some of these utilities.

    Args:
        auth: bool, optional, default: True
        docker: bool, optional, default: False
        shm: bool, optional, default: True
        mount_artifacts_store: bool, optional, default: True
        collect_artifacts: bool, optional, default: True
        collect_logs: bool, optional, default: True
        collect_resources: bool, optional, default: True
        auto_resume: bool, optional, default: True
        log_level: str, optional
        sidecar: V1PolyaxonSidecarContainer, optional

    ## YAML usage

    ```yaml
    >>> plugins:
    >>>   auth:
    >>>   docker:
    >>>   shm:
    >>>   mountArtifactsStore:
    >>>   collectArtifacts:
    >>>   collectLogs:
    >>>   collectResources:
    >>>   autoResume:
    >>>   externalHost:
    >>>   logLevel:
    >>>   sidecar:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Plugins
    >>> plugins = V1Plugins(
    >>>     auth=False,
    >>>     docker=True,
    >>>     shm=True.
    >>>     mount_artifacts_store=True,
    >>>     collect_artifacts=False,
    >>>     collect_logs=False,
    >>>     collect_resources=False
    >>>     auto_resume=False,
    >>>     external_host=False,
    >>>     log_level="INFO",
    >>> )
    ```

    ## Fields

    ### auth

    <blockquote class="light">
    This plugin is enabled by default in Polyaxon deployments with user management.
    </blockquote>

    By default, Polyaxon will create an auth context for each operation, this removes the overhead
    to think about how you can pass tokens to your runs,
    or the need to create secrets to load the token from during the run time.

    The auth context that Polyaxon provides is not only specific to the user who
    executed the run, but it also impersonates similar user access rights, it has the same scopes
    and restrictions the user usually has within the context of the project
    managing the run.
    This is important to make sure the API calls made during the run
    by the user's code have the right access to the resources requested.

    Oftentimes, users might not need to use an authenticated client inside their containers,
    in that case they can disable this plugin.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   auth: false
    ```

    ### docker

    <blockquote class="light">This plugin is disabled by default.</blockquote>

    This plugin exposes a docker socket volume to your run container.

    N.B. use this plugin carefully, you might also need to check with your devops
    team before using it, it requires docker.sock of the host to be mounted
    which is often rejected by OPA.

    To enable this plugin:

    ```yaml
    >>> plugins:
    >>>   docker: true
    ```

    ### shm

    <blockquote class="light">This plugin is enabled by default.</blockquote>

    This plugin mounts an tmpfs volume to /dev/shm.
    This will set /dev/shm size to half of the RAM of node.
    By default, /dev/shm is very small, only 64MB.
    Some experiments/jobs will fail due to the lack of shared memory,
    such as some experiments running on Pytorch.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   shm: false
    ```

    ### mountArtifactsStore

    <blockquote class="light">This plugin is disabled by default.</blockquote>

    this plugin allows to request the default artifacts store and mount it to the main container
    without adding the connection reference name to the `connections` section.

    This is usually very useful than setting the `connections` section as it make the component
    more generic and will not break if the artifacts store name changes.

    ### collectArtifacts

    <blockquote class="light">This plugin is enabled by default.</blockquote>

    By default, Polyaxon will collect all artifacts and outputs that you share in the
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
    Polyaxon expose a [context](/docs/core//context/) that get resolved during
    the compilation time, you can just use
    "{{run_artifacts_path}}" global variable and it will be resolved automatically.

    Example:

    ```yaml
    >>> run:
    >>>   kind: job
    >>>   container:
    >>>     command: "cp /some/know/path/file {{run_artifacts_path}}/file"

    ```

    For more information about the context, please check [context](/docs/core/context/)

    ### collectLogs

    <blockquote class="light">This plugin is enabled by default.</blockquote>

    By default, Polyaxon will collect all logs related to your runs before deleting
    the resource on the clusters. This ensures that your cluster(s) are kept clean and no resources
    are actively putting pressure on the API server.

    Sometimes you might want to avoid collecting logs for some runs, for example test or debug jobs.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   collectLogs: false
    ```

    ### collectResources

    <blockquote class="light">This plugin is enabled by default.</blockquote>

    By default, Polyaxon will collect all Mem/CPU/GPU resources
    for your runs that use the python client.

    Sometimes you might want to avoid collecting this information for some runs,
    for example test or debug jobs.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   collectResources: false
    ```

    ### autoResume

    <blockquote class="light">This plugin is enabled by default.</blockquote>

    By default, Polyaxon will resume from collecting metrics/outputs/artifacts
    if a run fails and retries or if the user resume a run.

    To disable this plugin:

    ```yaml
    >>> plugins:
    >>>   autoResume: false
    ```

    ### externalHost
    <blockquote class="light">Default is False.</blockquote>
    In some edge cases where the auxiliaries and/or the main container cannot reach the API/Streams
    services via the internal networking interface, you can enable this flag to tell Polyaxon
    resolve the external host instead of the default behavior with the in-cluster host.

    ```yaml
    >>> plugins:
    >>>   externalHost: true
    ```

    ### logLevel

    <blockquote class="light">Default is None.</blockquote>

    If you want to control the log level of your runs in a similar way locally and on the cluster,
    you can either use env vars or this plugin to share the same log level with all containers
    running in your operation.

    ```yaml
    >>> plugins:
    >>>   logLevel: warning
    ```

    ### sidecar

    <blockquote class="light">Default is None.</blockquote>

    To override the default global sidecar configuration.

    ```yaml
    >>> plugins:
    >>>   sidecar:
    >>>     syncInterval: 60
    ```
    """

    IDENTIFIER = "plugins"
    SCHEMA = PluginsSchema
    REDUCED_ATTRIBUTES = [
        "auth",
        "docker",
        "shm",
        "mountArtifactsStore",
        "collectArtifacts",
        "collectLogs",
        "collectResources",
        "autoResume",
        "syncStatuses",
        "externalHost",
        "logLevel",
        "sidecar",
        "notifications",
    ]
