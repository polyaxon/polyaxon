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
    description = fields.Str(required=True)
    kind = fields.Str(
        required=True, validate=validate.OneOf(V1ConnectionKind.allowable_values)
    )
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
    types of external system and resources to your operations.

    All connections in Polyaxon are typed, and some of them have special built-in handlers
    to automatically connect and load information.

    Connections allows to set the definition of a connection by someone who has knowledge about it,
    and end users, e.g. data scientist can just reference the name of the connection to use
    without dealing with the configurations every time.

    Connections are not required to mount secret or configuration,
    in fact users can do it the Kubernetes way, using volumes and env vars,
    but this mean you are exposing the service to very few team members who know about Kubernetes,
    in some advance you will have to leverage the low level Kuberentes API,
    but for most interactions, using the connection is much simpler,
    in the same it's much simpler to define service accounts or image pull secrets instead of
    defining all the volumes and mounting them to containers.

    Polyaxon, for some distributions, will exposes analytics about how often a connections is user,
    jobs that requested those connections, profile and run time to optimize the access,
    and additional RBAC and ACL rules to control who can access the connections.


    Args:
         name: str
         description: str, optional
         kind: str, one of ["host_path", "volume_claim", "gcs", "s3", "wasb", "registry", "git",
                            "aws", "gcp", "azure", "mysql", "postgres", "oracle", "vertica",
                            "sqlite", "mssql", "redis", "presto", "mongo", "cassandra", "ftp",
                            "grpc", "hdfs", "http", "pig_cli", "hive_cli", "hive_metastore",
                            "hive_server2", "jdbc", "jenkins", "samba", "snowflake", "ssh",
                            "cloudant", "databricks", "segment", "slack", "discord", "mattermost",
                            "pager_duty", "hipchat", "webhook", "custom"]
        schema: dict, optional
        secret: str, optional
        config_map: str, optional


    ## Yaml usage

    ```yaml
    >>> connections:
    >>>   - name: repo-test
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
    ```

    ## Fields

    ### name

    The connection name must be unique within an organization.
    User can use this unique name to reference a connection in their components and operations.

    An end user does not need to know about how to mount secrets and configurations
    to access a dataset for example, they can just reference the name of the connection.

    ### description

    A short description of the purpose of the connection for other users to learn
    about purpose of this connection.

    For example, "s3 bucket with radio images"

    ### kind

    the kind of the connection. Beside the fact that the Polyaxon
    has built-in handlers for several connections, user can build their own handlers,
    for example you can create a handler for pulling data from a database
    or data lake based on the kind.

    Polyaxon will show a small connection logo for some types in the dashboard.

    Polyaxon exposes this list of connection kinds:

        *  HOST_PATH: "host_path"
        *  VOLUME_CLAIM: "volume_claim"
        *  GCS: "gcs"
        *  S3: "s3"
        *  WASB: "wasb"
        *  REGISTRY: "registry"
        *  GIT: "git"
        *  AWS: "aws"
        *  GCP: "gcp"
        *  AZURE: "azure"
        *  MYSQL: "mysql"
        *  POSTGRES: "postgres"
        *  ORACLE: "oracle"
        *  VERTICA: "vertica"
        *  SQLITE: "sqlite"
        *  MSSQL: "mssql"
        *  REDIS: "redis"
        *  PRESTO: "presto"
        *  MONGO: "mongo"
        *  CASSANDRA: "cassandra"
        *  FTP: "ftp"
        *  GRPC: "grpc"
        *  HDFS: "hdfs"
        *  HTTP: "http"
        *  PIG_CLI: "pig_cli"
        *  HIVE_CLI: "hive_cli"
        *  HIVE_METASTORE: "hive_metastore"
        *  HIVE_SERVER2: "hive_server2"
        *  JDBC: "jdbc"
        *  JENKINS: "jenkins"
        *  SAMBA: "samba"
        *  SNOWFLAKE: "snowflake"
        *  SSH: "ssh"
        *  CLOUDANT: "cloudant"
        *  DATABRICKS: "databricks"
        *  SEGMENT: "segment"
        *  SLACK: "slack"
        *  DISCORD: "discord"
        *  MATTERMOST: "mattermost"
        *  PAGER_DUTY: "pager_duty"
        *  HIPCHAT: "hipchat"
        *  WEBHOOK: "webhook"
        *  CUSTOM: "custom"

    Polyaxon can also automatically handle these connection kinds:
    [HOST_PATH, VOLUME_CLAIM, GCS, S3, WASB, REGISTRY, GIT, AWS, GCP, AZURE].

    ### schema

    If you want to leverage some built-in functionalities in Polyaxon, automatic management of outputs,
    initializers for preparing code from git repos, loading data from S3/GCS/Azure/Volumes/Paths,
    or pushing container images to a registry,
    the schema is how Polyaxon authenticate the containers that will handle that logic.

    If you opt-out of using those functionality, you can leave this field empty or
    you can expose any key/value object.

     * Schema for volumes:
        * volumeClaim: volume claim name.
        * mountPath: path where to mount the volume content in the container
        * readOnly: if th volume should be mounted in read only mode.


        For more details please check the
        [Kubernets volume docs](https://kubernetes.io/docs/concepts/storage/volumes/)

        * Example definition:
            ```yaml
            >>> name: my-volume
            >>> kind: volume_claim
            >>> schema:
            >>>   mountPath: "/tmp/outputs"
            >>>   volumeClaim: "outputs-2-pvc"
            ```
        * Example usage as init param:
            ```yaml
            >>> params:
            >>>   data: {connection: "my-volume", init: true}
            ```

            Specific files:

            ```yaml
            >>> params:
            >>>   data: {
            >>>     connection: "my-volume",
            >>>     init: true,
            >>>     artifacts: {'files': ['file1', 'path/to/file2']}
            >>>   }
            ```

        * Example exposing the connection as an init container with custom container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   init: [{connection: "my-volume", container: {name: my-own-container, image: ...}}]
            >>>   container:
            ```

        * Example exposing the connection inside the main container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   connections: ["my-volume"]
            >>>   container:
            ```
    * Schema for host path:
        * host_path: the host path.
        * mount_path: path where to mount the volume content in the container
        * read_only: if th volume should be mounted in read only mode.

        For more details please check the
        [Kubernets volume docs](https://kubernetes.io/docs/concepts/storage/volumes/)

        * Example definition:
            ```yaml
            >>> name: my-volume
            >>> kind: host_path
            >>> schema:
            >>>   mountPath: "/tmp/outputs"
            >>>   hostPath: "/foo/bar"
            ```
        * Example usage as init param:
            ```yaml
            >>> params:
            >>>   data: {connection: "my-volume", init: true}
            ```

            Specific files:

            ```yaml
            >>> params:
            >>>   data: {
            >>>     connection: "my-volume",
            >>>     init: true,
            >>>     artifacts: {'files': ['file1', 'path/to/file2']}
            >>>   }
            ```

        * Example exposing the connection as an init container with custom container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   init: [{connection: "my-volume", container: {name: my-own-container, image: ...}}]
            >>>   container:
            ```

        * Example exposing the connection inside the main container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   connections: ["my-volume"]
            >>>   container:
            ```

     * Schema for S3/GCS/Azure Blob:
        * bucket: the bucket you want to expose in this connection.

        * Example definition:
            ```yaml
            >>> name: azure
            >>> kind: wasb
            >>> schema:
            >>>   bucket: "wasbs://logs@plxtest.blob.core.windows.net/"
            >>>  secret:
            >>>    name: "az-secret"
            ```
        * Example usage as init param:
            ```yaml
            >>> params:
            >>>   data: {connection: "azure", init: true}
            ```

            Specific files:

            ```yaml
            >>> params:
            >>>   data: {
            >>>     connection: "azure",
            >>>     init: true,
            >>>     artifacts: {'files': ['file1', 'path/to/file2']}
            >>>   }
            ```

        * Example exposing the connection as an init container with custom container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   init: [{connection: "azure", container: {name: my-own-container, image: ...}}]
            >>>   container:
            ```

        * Example exposing the connection inside the main container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   connections: ["azure"]
            >>>   container:
            ```

     * Schema for git connections:
        * url: the git repo to initialize. Note it;s possible not to define a repo and do
               it manually for every run, but you will not get the granularity control.

        * Example:
            ```yaml
            >>> name: repo-test
            >>> kind: git
            >>> schema:
            >>>   url: https://gitlab.com/org/test
            >>> secret:
            >>>   name: "gitlab-connection"
            ```
        * Example usage as init param:
            ```yaml
            >>> params:
            >>>   data: {connection: "repo-test", init: true}
            ```

            Specific branch or commit:

            ```yaml
            >>> params:
            >>>   data: {
            >>>     connection: "repo-test",
            >>>     init: true,
            >>>     git: {revision: branch2}
            >>>   }
            ```

            Overriding the default git url:

            ```yaml
            >>> params:
            >>>   data: {
            >>>     connection: "repo-test",
            >>>     init: true,
            >>>     git: {url: https://new.com}
            >>>   }
            ```

        * Example exposing the connection as an init container with custom container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   init: [{connection: "repo-test", container: {name: my-own-container, image: ...}}]
            >>>   container:
            ```

        * Example exposing the connection inside the main container:
            ```yaml
            >>> run:
            >>>   kind: service
            >>>   connections: ["repo-test"]
            >>>   container:
            ```

     * Schema for registry connections:
        * bucket: the bucket you want to expose in this connection.
        * Example using kaniko:
            ```yaml
            >>> name: docker-connection-kaniko
            >>> kind: registry
            >>> schema:
            >>>   url: https://myregistry.com/org/repo
            >>> secret:
            >>>   name: docker-conf
            >>>   mountPath: /kaniko/.docker
            ```
        * Example using dockerizer:
            ```yaml
            >>> name: docker-connection-dockerizer
            >>> kind: registry
            >>> schema:
            >>>   url: https://myregistry.com/org/repo
            >>> secret:
            >>>   name: docker-conf
            >>>   mountPath: /root/.docke
            ```

        In both example we are mounting the same secret but to 2 different paths,
        if you are using the dockerizer for instance with a specific user
        UID you might also want to change the path.

    ### secret
    We assume that each connection will only need to access to at most one secret.
    If you are building a specific handler for a connection,
    this is where you will need to expose the necessary paths or environment variables needed
    to make the http/grpc connection.

    In many cases you might not need to expose any secret, for instance for volumes and hot paths.

    ### configMap
    We assume that each connection will only need to access to at most one config map.
    Similar logic for the secret, if you need to expose more information to connect to a service,
    you can reference a config_map.
    """
    IDENTIFIER = "connection"
    SCHEMA = ConnectionTypeSchema
    REDUCED_ATTRIBUTES = ["name", "kind", "schema", "secret", "configMap"]

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
            return self.schema.mount_path
        if self.is_bucket:
            return self.schema.bucket

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
