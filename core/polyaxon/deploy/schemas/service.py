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

from marshmallow import EXCLUDE, fields

from polyaxon.deploy.schemas.celery import CelerySchema
from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class ServiceSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    image = fields.Str(allow_none=True)
    image_tag = fields.Str(allow_none=True)
    image_pull_policy = fields.Str(allow_none=True)
    replicas = fields.Int(allow_none=True)
    concurrency = fields.Int(allow_none=True)
    resources = SwaggerField(cls=k8s_schemas.V1ResourceRequirements, allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @staticmethod
    def schema_config():
        return Service


class Service(BaseConfig):
    SCHEMA = ServiceSchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "image",
        "imageTag",
        "imagePullPolicy",
        "replicas",
        "concurrency",
        "resources",
    ]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
    ):
        self.enabled = enabled
        self.image = image
        self.image_tag = image_tag
        self.image_pull_policy = image_pull_policy
        self.replicas = replicas
        self.concurrency = concurrency
        self.resources = resources


class WorkerServiceSchema(ServiceSchema):
    celery = fields.Nested(CelerySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return WorkerServiceConfig


class WorkerServiceConfig(Service):
    SCHEMA = WorkerServiceSchema
    REDUCED_ATTRIBUTES = Service.REDUCED_ATTRIBUTES + ["celery"]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        celery=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.celery = celery


class HelperServiceSchema(ServiceSchema):
    sleep_interval = fields.Int(allow_none=True)
    sync_interval = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return HelperServiceConfig


class HelperServiceConfig(Service):
    SCHEMA = HelperServiceSchema
    REDUCED_ATTRIBUTES = Service.REDUCED_ATTRIBUTES + [
        "sleepInterval",
        "syncInterval",
    ]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        sleep_interval=None,
        sync_interval=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.sleep_interval = sleep_interval
        self.sync_interval = sync_interval


class AgentServiceSchema(ServiceSchema):
    instance = fields.String(allow_none=True)
    token = fields.String(allow_none=True)
    is_replica = fields.Bool(allow_none=True)
    compressed_logs = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return AgentServiceConfig


class AgentServiceConfig(Service):
    SCHEMA = AgentServiceSchema
    REDUCED_ATTRIBUTES = Service.REDUCED_ATTRIBUTES + [
        "instance",
        "token",
        "isReplica",
        "compressedLogs",
    ]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        instance=None,
        token=None,
        is_replica=None,
        compressed_logs=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.instance = instance
        self.token = token
        self.is_replica = is_replica
        self.compressed_logs = compressed_logs


class OperatorServiceSchema(ServiceSchema):
    skip_crd = fields.Bool(allow_none=True, data_key="skipCRD")
    use_crd_v1beta1 = fields.Bool(allow_none=True, data_key="useCRDV1Beta1")

    @staticmethod
    def schema_config():
        return OperatorServiceConfig


class OperatorServiceConfig(Service):
    SCHEMA = OperatorServiceSchema
    REDUCED_ATTRIBUTES = Service.REDUCED_ATTRIBUTES + ["skipCRD", "useCRDV1Beta1"]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        skip_crd=None,
        use_crd_v1beta1=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.skip_crd = skip_crd
        self.use_crd_v1beta1 = use_crd_v1beta1


class ApiServiceSchema(ServiceSchema):
    service = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ApiServiceConfig


class ApiServiceConfig(Service):
    SCHEMA = ApiServiceSchema

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        service=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.service = service


class HooksSchema(ServiceSchema):
    load_fixtures = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return HooksConfig


class HooksConfig(Service):
    SCHEMA = HooksSchema
    REDUCED_ATTRIBUTES = Service.REDUCED_ATTRIBUTES + ["loadFixtures"]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        concurrency=None,
        resources=None,
        load_fixtures=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.load_fixtures = load_fixtures


class ThirdPartyServiceSchema(ServiceSchema):
    enabled = fields.Bool(allow_none=True)
    persistence = fields.Dict(allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(allow_none=True), allow_none=True)

    @staticmethod
    def schema_config():
        return ThirdPartyService


class ThirdPartyService(Service):
    SCHEMA = ThirdPartyServiceSchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "image",
        "imageTag",
        "imagePullPolicy",
        "replicas",
        "concurrency",
        "resources",
        "persistence",
        "nodeSelector",
        "affinity",
        "tolerations",
    ]

    def __init__(
        self,
        enabled=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        resources=None,
        persistence=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
    ):
        super().__init__(
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            resources=resources,
        )
        self.enabled = enabled
        self.persistence = persistence
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations


class PostgresqlSchema(ThirdPartyServiceSchema):
    postgres_user = fields.Str(allow_none=True)
    postgres_password = fields.Str(allow_none=True)
    postgres_database = fields.Str(allow_none=True)
    conn_max_age = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return PostgresqlConfig


class PostgresqlConfig(ThirdPartyService):
    SCHEMA = PostgresqlSchema
    REDUCED_ATTRIBUTES = ThirdPartyService.REDUCED_ATTRIBUTES + [
        "postgresUser",
        "postgresPassword",
        "postgresDatabase",
        "connMaxAge",
    ]

    def __init__(
        self,
        enabled=None,
        postgres_user=None,
        postgres_password=None,
        postgres_database=None,
        conn_max_age=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        resources=None,
        persistence=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_database = postgres_database
        self.conn_max_age = conn_max_age


class RedisSchema(ThirdPartyServiceSchema):
    image = fields.Raw(allow_none=True)
    non_broker = fields.Bool(allow_none=True)
    use_password = fields.Bool(allow_none=True)
    password = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RedisConfig


class RedisConfig(ThirdPartyService):
    SCHEMA = RedisSchema
    REDUCED_ATTRIBUTES = ThirdPartyService.REDUCED_ATTRIBUTES + [
        "nonBroker",
        "usePassword",
        "password",
    ]

    def __init__(
        self,
        enabled=None,
        non_broker=None,
        use_password=None,
        password=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        resources=None,
        persistence=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        self.non_broker = non_broker
        self.use_password = use_password
        self.password = password


class RabbitmqSchema(ThirdPartyServiceSchema):
    rabbitmq_username = fields.Str(allow_none=True)
    rabbitmq_password = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RabbitmqConfig


class RabbitmqConfig(ThirdPartyService):
    SCHEMA = RabbitmqSchema
    REDUCED_ATTRIBUTES = ThirdPartyService.REDUCED_ATTRIBUTES + [
        "rabbitmqUsername",
        "rabbitmqPassword",
    ]

    def __init__(
        self,
        enabled=None,
        rabbitmq_username=None,
        rabbitmq_password=None,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        replicas=None,
        resources=None,
        persistence=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
    ):
        super().__init__(
            enabled=enabled,
            image=image,
            image_tag=image_tag,
            image_pull_policy=image_pull_policy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password


class ExternalServiceSchema(BaseCamelSchema):
    user = fields.Str(allow_none=True)
    password = fields.Str(allow_none=True)
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    database = fields.Str(allow_none=True)
    use_password = fields.Bool(allow_none=True)
    conn_max_age = fields.Int(allow_none=True)
    pgbouncer = fields.Dict(allow_none=True)
    options = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ExternalService


class ExternalService(BaseConfig):
    SCHEMA = ExternalServiceSchema
    REDUCED_ATTRIBUTES = [
        "user",
        "password",
        "host",
        "port",
        "database",
        "usePassword",
        "connMaxAge",
        "pgbouncer",
        "options",
    ]

    def __init__(
        self,
        user=None,
        password=None,
        host=None,
        port=None,
        database=None,
        use_password=None,
        conn_max_age=None,
        pgbouncer=None,
        options=None,
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.use_password = use_password
        self.conn_max_age = conn_max_age
        self.pgbouncer = pgbouncer
        self.options = options


class ExternalBackendSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    backend = fields.Str(allow_none=True)
    options = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ExternalBackend


class ExternalBackend(BaseConfig):
    SCHEMA = ExternalBackendSchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "backend",
        "options",
    ]

    def __init__(
        self,
        enabled=None,
        backend=None,
        options=None,
    ):
        self.enabled = enabled
        self.backend = backend
        self.options = options


class AuthServicesSchema(BaseCamelSchema):
    github = fields.Nested(ExternalBackendSchema, allow_none=True)
    gitlab = fields.Nested(ExternalBackendSchema, allow_none=True)
    bitbucket = fields.Nested(ExternalBackendSchema, allow_none=True)
    google = fields.Nested(ExternalBackendSchema, allow_none=True)
    saml = fields.Nested(ExternalBackendSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return AuthServicesConfig


class AuthServicesConfig(BaseConfig):
    SCHEMA = AuthServicesSchema
    REDUCED_ATTRIBUTES = [
        "github",
        "gitlab",
        "bitbucket",
        "google",
        "saml",
    ]

    def __init__(
        self,
        github=None,
        gitlab=None,
        bitbucket=None,
        google=None,
        saml=None,
    ):
        self.github = github
        self.gitlab = gitlab
        self.bitbucket = bitbucket
        self.google = google
        self.saml = saml


class ExternalServicesSchema(BaseCamelSchema):
    redis = fields.Nested(ExternalServiceSchema, allow_none=True)
    rabbitmq = fields.Nested(ExternalServiceSchema, allow_none=True)
    postgresql = fields.Nested(ExternalServiceSchema, allow_none=True)
    gateway = fields.Nested(ExternalServiceSchema, allow_none=True)
    api = fields.Nested(ExternalServiceSchema, allow_none=True)
    transactions = fields.Nested(ExternalBackendSchema, allow_none=True)
    analytics = fields.Nested(ExternalBackendSchema, allow_none=True)
    metrics = fields.Nested(ExternalBackendSchema, allow_none=True)
    errors = fields.Nested(ExternalBackendSchema, allow_none=True)
    auth = fields.Nested(AuthServicesSchema, allow_none=True)
    allowed_versions = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return ExternalServicesConfig


class ExternalServicesConfig(BaseConfig):
    SCHEMA = ExternalServicesSchema
    REDUCED_ATTRIBUTES = [
        "redis",
        "rabbitmq",
        "postgresql",
        "gateway",
        "api",
        "transactions",
        "analytics",
        "metrics",
        "errors",
        "auth",
        "allowedVersions",
    ]

    def __init__(
        self,
        redis=None,
        rabbitmq=None,
        postgresql=None,
        gateway=None,
        api=None,
        transactions=None,
        analytics=None,
        metrics=None,
        errors=None,
        auth=None,
        allowed_versions=None,
    ):
        self.redis = redis
        self.rabbitmq = rabbitmq
        self.postgresql = postgresql
        self.gateway = gateway
        self.api = api
        self.transactions = transactions
        self.analytics = analytics
        self.metrics = metrics
        self.errors = errors
        self.auth = auth
        self.allowed_versions = allowed_versions
