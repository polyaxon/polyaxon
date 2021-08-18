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
from typing import Optional

import polyaxon_sdk

from marshmallow import fields, pre_load, validate

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    ConnectionSchema,
    K8sResourceSchema,
    V1BucketConnection,
    V1ClaimConnection,
    V1GitConnection,
    V1HostConnection,
    V1HostPathConnection,
)
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.types.k8s_resources import V1K8sResourceType


class ConnectionTypeSchema(BaseCamelSchema):
    name = fields.Str(required=True)
    kind = fields.Str(
        required=True, validate=validate.OneOf(V1ConnectionKind.allowable_values)
    )
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    schema = fields.Nested(ConnectionSchema, allow_none=True)
    secret = fields.Nested(K8sResourceSchema, allow_none=True)
    config_map = fields.Nested(K8sResourceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1ConnectionType

    @pre_load
    def pre_make(self, data, **kwargs):
        schema = data.get("schema")
        kind = data.get("kind")
        if schema and kind:
            schema["kind"] = "custom"
            if kind in V1ConnectionKind.BLOB_VALUES:
                schema["kind"] = V1BucketConnection.IDENTIFIER

            if kind == V1ConnectionKind.VOLUME_CLAIM:
                schema["kind"] = V1ClaimConnection.IDENTIFIER

            if kind == V1ConnectionKind.HOST_PATH:
                schema["kind"] = V1HostPathConnection.IDENTIFIER

            if kind == V1ConnectionKind.REGISTRY:
                schema["kind"] = V1HostConnection.IDENTIFIER

            if kind == V1ConnectionKind.GIT:
                schema["kind"] = V1GitConnection.IDENTIFIER

        return data


class V1ConnectionType(BaseConfig, polyaxon_sdk.V1ConnectionType):
    """Connections are how Polyaxon connects several
    types of external systems and resources to your operations.

    All connections in Polyaxon are typed, and some of them have special built-in handlers
    to automatically connect and load information.

    Using connections you can define the boilerplate required
    to connect a volume, a blob storage once, secret definition for loading data from a data source.
    Rnd users, e.g. data scientist, can just reference the name of the connection to use it
    without dealing with the configuration every time.

    Connections are not required to mount secrets or configurations,
    in fact users can also mount secrets and volumes the Kubernetes way,
    but this mean you are exposing the service to very few team members who have
    the Kubernetes know-how, in some advance use-cases,
    you will have to leverage the low level Kubernetes API,
    but for most interactions, using the connection specification is much simpler,
    similar to how easy it is to define service accounts or image pull secrets instead of
    defining all the volumes and mounting them to the containers manually.

    For some distributions, Polyaxon will exposes:
        * Analytics about how often connections are used.
        * Jobs that requested those connections.
        * Profiling and runtime meta data to optimize access to those resources and connections.
        * Additional RBAC and ACL rules to control who can access the connections.

    Args:
         name: str
         description: str, optional
         tags: List[str], optional
         kind: str, Union[`host_path`, `volume_claim`, `gcs`, `s3`, `wasb`, `registry`, `git`,
                          `aws`, `gcp`, `azure`, `mysql`, `postgres`, `oracle`, `vertica`,
                          `sqlite`, `mssql`, `redis`, `presto`, `mongo`, `cassandra`, `ftp`,
                          `grpc`, `hdfs`, `http`, `pig_cli`, `hive_cli`, `hive_metastore`,
                          `hive_server2`, `jdbc`, `jenkins`, `samba`, `snowflake`, `ssh`,
                          `cloudant`, `databricks`, `segment`, `slack`, `discord`, `mattermost`,
                          `pagerduty`, `hipchat`, `webhook`, `custom`]
        schema: dict, optional
        secret: str, optional
        config_map: str, optional


    ## YAML usage

    ```yaml
    >>> artifactsStore:
    >>>   name: azure
    >>>   kind: wasb
    >>>   schema:
    >>>     bucket: "wasbs://test@container.blob.core.windows.net/"
    >>>   secret:
    >>>     name: "az-secret"
    >>> connections:
    >>>   - name: repo-test
    >>>     description: "some description"
    >>>     tags: ["tag1", "tag2"]
    >>>     kind: git
    >>>     schema:
    >>>       url: https://gitlab.com/org/test
    >>>     secret:
    >>>       name: "gitlab-connection"
    >>>   - name: docker-connection
    >>>     description: "some description"
    >>>     kind: registry
    >>>     schema:
    >>>       url: org/repo
    >>>     secret:
    >>>       name: docker-conf
    >>>       mountPath: /kaniko/.docker
    >>>   - name: my-slack
    >>>     kind: slack
    >>>     secret:
    >>>       name: my-slack
    ```

    ## Fields

    ### name

    The connection name must be unique within an organization.
    User can use this unique name to reference a connection in their components and operations.

    An end user does not need to know about how to mount secrets and configurations
    to access a dataset for example, they can just reference the name of the connection.

    ### description

    A short description about the purpose of the connection for other users.

    For example, "s3 bucket with radio images"

    ### tags

    Tags to categorize the connection in the connections catalog table.

    ### kind

    the kind of the connection. Apart from the fact that Polyaxon
    has built-in handlers for several connections, user can build their own handlers,
    for example you can create a handler for pulling data from a database
    or a data lake based on a specific kind.

    Polyaxon will show a small connection logo for some types in the
    dashboard and analytics about the connection usage.

    Polyaxon exposes this list of connection kinds:
    [`host_path`, `volume_claim`, `gcs`, `s3`, `wasb`, `registry`, `git`, `aws`,
     `gcp`, `azure`, `mysql`, `postgres`, `oracle`, `vertica`,
     `sqlite`, `mssql`, `redis`, `presto`, `mongo`, `cassandra`, `ftp`,
     `grpc`, `hdfs`, `http`, `pig_cli`, `hive_cli`, `hive_metastore`,
     `hive_server2`, `jdbc`, `jenkins`, `samba`, `snowflake`, `ssh`,
     `cloudant`, `databricks`, `segment`, `slack`, `discord`, `mattermost`,
     `pagerduty`, `hipchat`, `webhook`, `custom`]

    Polyaxon can also automatically handle these connection kinds:
    [`host_path`, `volume_claim`, `gcs`, `s3`, `wasb`, `registry`, `git`]

    ### schema

    In order to leverage some built-in functionalities in Polyaxon,
    e.g. automatic management of outputs, initializers for cloning code from git repos,
    loading data from S3/GCS/Azure/Volumes/Paths, or pushing container images to a registry,
    the schema is how Polyaxon knows how to authenticate the containers that will handle that logic.

    If you opt-out of using those functionalities, you can leave this field empty or
    you can expose any key/value object you want for your own custom handlers.

    For more details please check connection schema section for the built-in handlers:
        * [artifacts connections](/docs/setup/connections/artifacts/)
        * [git connections](/docs/setup/connections/git/)
        * [docker registry connections](/docs/setup/connections/registry/)

    ### secret

    We assume that each connection will only need to access to at most one secret.
    If you are building a specific handler for a connection,
    this is where you will need to expose the necessary paths or environment variables needed
    to make the http/grpc connection.

    In many cases you might not need to expose any secret, for instance for volumes and host paths.

    The connection secret schema has 3 fields:

        * name: str, required, the name of the secret,
                this is the minimum to tell Polyaxon to mount that secret
                whenever the connection is referenced.
        * mountPath: str, optional, if you prefer to mount the secret as a volume
                     instead of exposing its items as environment variables.
        * items: List[str], optional, if you only want to expose a subset
                 of the items in the secret.

    Example slack connection

    ```yaml
    >>> name: my-slack
    >>> kind: slack
    >>> secret:
    >>>   name: my-slack
    ```

    Example docker connection with mountPath

    ```yaml
    >>> kind: registry
    >>> schema:
    >>>   url: registry.com/org/repo
    >>> secret:
    >>>   name: docker-conf
    >>>   mountPath: /kaniko/.docker
    ```

    ### configMap

    We assume that each connection will only need to access to at most one config map.
    Similar logic for the secret, if you need to expose more information to connect to a service,
    you can reference a config map.

    In many cases you might not need to expose any config map.

    The connection configMap schema has 3 fields:

        * name: str, required, the name of the configMap,
                this is the minimum to tell Polyaxon to mount that configMap
                whenever the connection is referenced.
        * mountPath: str, optional, if you prefer to mount the configMap as a volume
                     instead of exposing its items as environment variables.
        * items: List[str], optional, if you only want to expose a subset
                 of the items in the configMap.
    """

    IDENTIFIER = "connection"
    SCHEMA = ConnectionTypeSchema
    REDUCED_ATTRIBUTES = [
        "name",
        "kind",
        "description",
        "tags",
        "schema",
        "secret",
        "configMap",
    ]

    @classmethod
    def from_model(cls, model) -> "V1ConnectionType":
        schema = model.schema
        secret = model.secret
        config_map = model.config_map
        if hasattr(schema, "to_dict"):
            schema = schema.to_dict()
        if hasattr(secret, "to_dict"):
            secret = secret.to_dict()
        if hasattr(config_map, "to_dict"):
            config_map = config_map.to_dict()
        return V1ConnectionType.from_dict(
            {
                "name": model.name,
                "kind": model.kind,
                "schema": schema,
                "secret": secret,
                "configMap": config_map,
            }
        )

    @property
    def store_path(self) -> str:
        if self.is_mount:
            return self.schema.mount_path.rstrip("/")
        if self.is_bucket:
            bucket = self.schema.bucket.rstrip("/")
            if self.is_wasb:
                from polyaxon.parser.parser import parse_wasbs_path

                return parse_wasbs_path(bucket).get_container_path()
            return bucket

    @property
    def is_mount(self) -> bool:
        return V1ConnectionKind.is_mount(self.kind)

    @property
    def is_artifact(self) -> bool:
        return V1ConnectionKind.is_artifact(self.kind)

    @property
    def is_host_path(self) -> bool:
        return V1ConnectionKind.is_host_path(self.kind)

    @property
    def is_volume_claim(self) -> bool:
        return V1ConnectionKind.is_volume_claim(self.kind)

    @property
    def is_bucket(self) -> bool:
        return V1ConnectionKind.is_bucket(self.kind)

    @property
    def is_gcs(self) -> bool:
        return self.kind == V1ConnectionKind.GCS

    @property
    def is_s3(self) -> bool:
        return self.kind == V1ConnectionKind.S3

    @property
    def is_wasb(self) -> bool:
        return V1ConnectionKind.is_wasb(self.kind)

    def get_secret(self) -> Optional[V1K8sResourceType]:
        if self.secret:
            return V1K8sResourceType(name=self.secret.name, schema=self.secret)
        return None

    def get_config_map(self) -> Optional[V1K8sResourceType]:
        if self.config_map:
            return V1K8sResourceType(name=self.config_map.name, schema=self.config_map)
        return None
