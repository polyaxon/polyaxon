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

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.deploy.schemas.deployment_types import DeploymentTypes
from polyaxon.deploy.schemas.email import EmailSchema
from polyaxon.deploy.schemas.ingress import IngressSchema
from polyaxon.deploy.schemas.intervals import IntervalsSchema
from polyaxon.deploy.schemas.rbac import RBACSchema
from polyaxon.deploy.schemas.root_user import RootUserSchema
from polyaxon.deploy.schemas.security_context import SecurityContextSchema
from polyaxon.deploy.schemas.service import (
    AgentServiceSchema,
    ApiServiceSchema,
    DockerRegistrySchema,
    ExternalServicesSchema,
    HelperServiceSchema,
    HooksSchema,
    PostgresqlSchema,
    RabbitmqSchema,
    RedisSchema,
    ServiceSchema,
    WorkerServiceSchema,
)
from polyaxon.deploy.schemas.service_types import ServiceTypes
from polyaxon.deploy.schemas.ssl import SSLSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.types import ConnectionTypeSchema


def check_redis(redis, external_services):
    redis_disabled = redis.enabled is False if redis else False
    external_redis = None
    if external_services:
        external_redis = external_services.redis

    if redis_disabled and not external_redis:
        raise ValidationError(
            "A redis instance is required, please enable the in-cluster redis, "
            "or provide an external instance."
        )


def check_postgres(postgresql, external_services):
    postgresql_disabled = postgresql.enabled is False if postgresql else False
    external_postgresql = None
    if external_services:
        external_postgresql = external_services.postgresql

    if postgresql_disabled and not external_postgresql:
        raise ValidationError(
            "A postgresql instance is required, "
            "please enable the in-cluster postgresql, "
            "or provide an external instance."
        )


def check_rabbitmq(rabbitmq, external_services, broker):
    rabbitmq_disabled = rabbitmq.enabled is False if rabbitmq else False
    external_rabbitmq = None
    rabbitmq_borker = broker != "redis"
    if external_services:
        external_rabbitmq = external_services.rabbitmq

    if rabbitmq_disabled and rabbitmq_borker and not external_rabbitmq:
        raise ValidationError(
            "Rabbitmq is used as a broker, "
            "an instance is required, "
            "please enable the in-cluster rabbitmq, "
            "or provide an external instance."
        )


class DeploymentSchema(BaseCamelSchema):
    deployment_type = fields.Str(
        allow_none=True, validate=validate.OneOf(DeploymentTypes.VALUES)
    )
    deployment_version = fields.Str(allow_none=True)
    namespace = fields.Str(allow_none=True)
    rbac = fields.Nested(RBACSchema, allow_none=True)
    polyaxon_secret = fields.Str(allow_none=True)
    internal_token = fields.Str(allow_none=True)
    password_length = fields.Int(allow_none=True)
    ssl = fields.Nested(SSLSchema, allow_none=True)
    encryption_secret = fields.Str(allow_none=True)
    service_type = fields.Str(
        allow_none=True, validate=validate.OneOf(ServiceTypes.VALUES)
    )
    admin_view_enabled = fields.Bool(allow_none=True)
    timezone = fields.Str(allow_none=True)
    environment = fields.Str(allow_none=True)
    ingress = fields.Nested(IngressSchema, allow_none=True)
    user = fields.Nested(RootUserSchema, allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(allow_none=True), allow_none=True)
    affinity = fields.Dict(allow_none=True)
    limit_resources = fields.Bool(allow_none=True)
    global_replicas = fields.Int(allow_none=True)
    global_concurrency = fields.Int(allow_none=True)
    gateway = fields.Nested(ApiServiceSchema, allow_none=True)
    api = fields.Nested(ApiServiceSchema, allow_none=True)
    streams = fields.Nested(ApiServiceSchema, allow_none=True)
    scheduler = fields.Nested(WorkerServiceSchema, allow_none=True)
    worker = fields.Nested(WorkerServiceSchema, allow_none=True)
    beat = fields.Nested(ServiceSchema, allow_none=True)
    agent = fields.Nested(AgentServiceSchema, allow_none=True)
    operator = fields.Nested(ServiceSchema, allow_none=True)
    init = fields.Nested(HelperServiceSchema, allow_none=True)
    sidecar = fields.Nested(HelperServiceSchema, allow_none=True)
    tables_hook = fields.Nested(ServiceSchema, allow_none=True)
    hooks = fields.Nested(HooksSchema, allow_none=True)
    postgresql = fields.Nested(PostgresqlSchema, allow_none=True)
    redis = fields.Nested(RedisSchema, allow_none=True)
    rabbitmq = fields.Nested(RabbitmqSchema, data_key="rabbitmq-ha", allow_none=True)
    broker = fields.Str(allow_none=True, validate=validate.OneOf(["redis", "rabbitmq"]))
    docker_registry = fields.Nested(
        DockerRegistrySchema, data_key="docker-registry", allow_none=True
    )
    email = fields.Nested(EmailSchema, allow_none=True)
    ldap = fields.Raw(allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    host_name = fields.Str(allow_none=True)
    allowed_hosts = fields.List(fields.Str(), allow_none=True)
    intervals = fields.Nested(IntervalsSchema, allow_none=True)
    artifacts_store = fields.Nested(ConnectionTypeSchema, allow_none=True,)
    connections = fields.List(fields.Nested(ConnectionTypeSchema), allow_none=True,)
    notification_connections = fields.List(
        fields.Nested(ConnectionTypeSchema), allow_none=True,
    )
    admin_models = fields.List(fields.Str(allow_none=True), allow_none=True)
    repos_access_token = fields.Str(allow_none=True)
    log_level = fields.Str(allow_none=True)
    tracker_backend = fields.Str(allow_none=True)
    security_context = fields.Nested(SecurityContextSchema, allow_none=True)
    external_services = fields.Nested(ExternalServicesSchema, allow_none=True)
    debug_mode = fields.Bool(allow_none=True)

    # Pending validation
    dns = fields.Raw(allow_none=True)
    plugins = fields.Raw(allow_none=True)

    @staticmethod
    def schema_config():
        return DeploymentConfig

    @validates_schema
    def validate_deployment(self, data, **kwargs):
        check_redis(data.get("redis"), data.get("external_services"))
        check_postgres(data.get("postgresql"), data.get("external_services"))
        check_rabbitmq(
            data.get("rabbitmq"), data.get("external_services"), data.get("broker")
        )


class DeploymentConfig(BaseConfig):
    SCHEMA = DeploymentSchema

    def __init__(
        self,
        deployment_type=None,
        deployment_version=None,
        namespace=None,
        rbac=None,
        polyaxon_secret=None,
        internal_token=None,
        password_length=None,
        ssl=None,
        encryption_secret=None,
        service_type=None,
        admin_view_enabled=None,
        timezone=None,
        environment=None,
        ingress=None,
        user=None,
        node_selector=None,
        tolerations=None,
        affinity=None,
        limit_resources=None,
        global_replicas=None,
        global_concurrency=None,
        gateway=None,
        api=None,
        streams=None,
        scheduler=None,
        worker=None,
        beat=None,
        agent=None,
        operator=None,
        init=None,
        sidecar=None,
        tables_hook=None,
        hooks=None,
        postgresql=None,
        redis=None,
        rabbitmq=None,
        broker=None,
        docker_registry=None,
        email=None,
        ldap=None,
        image_pull_secrets=None,
        host_name=None,
        allowed_hosts=None,
        intervals=None,
        artifacts_store=None,
        connections=None,
        notification_connections=None,
        admin_models=None,
        repos_access_token=None,
        log_level=None,
        tracker_backend=None,
        security_context=None,
        external_services=None,
        debug_mode=None,
        dns=None,
        plugins=None,
    ):
        check_redis(redis, external_services)
        check_postgres(postgresql, external_services)
        check_rabbitmq(rabbitmq, external_services, broker)
        self.deployment_type = deployment_type
        self.deployment_version = deployment_version
        self.namespace = namespace
        self.rbac = rbac
        self.polyaxon_secret = polyaxon_secret
        self.internal_token = internal_token
        self.password_length = password_length
        self.ssl = ssl
        self.dns = dns
        self.encryption_secret = encryption_secret
        self.service_type = service_type
        self.admin_view_enabled = admin_view_enabled
        self.timezone = timezone
        self.environment = environment
        self.ingress = ingress
        self.user = user
        self.node_selector = node_selector
        self.tolerations = tolerations
        self.affinity = affinity
        self.limit_resources = limit_resources
        self.global_replicas = global_replicas
        self.global_concurrency = global_concurrency
        self.gateway = gateway
        self.api = api
        self.streams = streams
        self.scheduler = scheduler
        self.worker = worker
        self.beat = beat
        self.agent = agent
        self.operator = operator
        self.init = init
        self.sidecar = sidecar
        self.tables_hook = tables_hook
        self.hooks = hooks
        self.postgresql = postgresql
        self.redis = redis
        self.rabbitmq = rabbitmq
        self.broker = broker
        self.docker_registry = docker_registry
        self.email = email
        self.ldap = ldap
        self.image_pull_secrets = image_pull_secrets
        self.host_name = host_name
        self.allowed_hosts = allowed_hosts
        self.intervals = intervals
        self.artifacts_store = artifacts_store
        self.connections = connections
        self.notification_connections = notification_connections
        self.admin_models = admin_models
        self.repos_access_token = repos_access_token
        self.log_level = log_level
        self.tracker_backend = tracker_backend
        self.security_context = security_context
        self.external_services = external_services
        self.debug_mode = debug_mode
        self.plugins = plugins
