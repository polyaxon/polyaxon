# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import EXCLUDE, fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema

from polyaxon_schemas.ops.environments.resources import K8SContainerResourcesSchema


class ServiceSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    image = fields.Str(allow_none=True)
    imageTag = fields.Str(allow_none=True)
    imagePullPolicy = fields.Str(allow_none=True)
    replicas = fields.Int(allow_none=True)
    concurrency = fields.Int(allow_none=True)
    resources = fields.Nested(K8SContainerResourcesSchema, allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @staticmethod
    def schema_config():
        return ServiceConfig


class ServiceConfig(BaseConfig):
    SCHEMA = ServiceSchema
    REDUCED_ATTRIBUTES = [
        'enabled',
        'image',
        'imageTag',
        'imagePullPolicy',
        'replicas',
        'concurrency',
        'resources'
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 concurrency=None,
                 resources=None):
        self.enabled = enabled
        self.image = image
        self.imageTag = imageTag
        self.imagePullPolicy = imagePullPolicy
        self.replicas = replicas
        self.concurrency = concurrency
        self.resources = resources


class ApiSchema(ServiceSchema):
    service = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ApiConfig


class ApiConfig(ServiceConfig):
    SCHEMA = ApiSchema
    REDUCED_ATTRIBUTES = ['replicas', 'namespace', 'statuses']

    def __init__(self,  # noqa
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 concurrency=None,
                 resources=None,
                 service=None):
        super(ApiConfig, self).__init__(
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources,
        )
        self.service = service


class EventMonitorsSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    namespace = fields.Nested(ServiceSchema, allow_none=True)
    statuses = fields.Nested(ServiceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return EventMonitorsConfig


class EventMonitorsConfig(BaseConfig):
    SCHEMA = EventMonitorsSchema
    REDUCED_ATTRIBUTES = ['replicas', 'namespace', 'statuses']

    def __init__(self, replicas=None, namespace=None, statuses=None):
        self.replicas = replicas
        self.namespace = namespace
        self.statuses = statuses


class HooksSchema(ServiceSchema):
    loadFixtures = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return HooksConfig


class HooksConfig(ServiceConfig):
    SCHEMA = HooksSchema
    REDUCED_ATTRIBUTES = ServiceConfig.REDUCED_ATTRIBUTES + ['loadFixtures']

    def __init__(self,  # noqa
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 concurrency=None,
                 resources=None,
                 loadFixtures=None):
        super(HooksConfig, self).__init__(
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            concurrency=concurrency,
            resources=resources)
        self.loadFixtures = loadFixtures


class ThirdPartyServiceSchema(ServiceSchema):
    enabled = fields.Bool(allow_none=True)
    persistence = fields.Dict(allow_none=True)
    nodeSelector = fields.Dict(allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(allow_none=True), allow_none=True)

    @staticmethod
    def schema_config():
        return ThirdPartyServiceConfig


class ThirdPartyServiceConfig(ServiceConfig):
    SCHEMA = ThirdPartyServiceSchema
    REDUCED_ATTRIBUTES = [
        'enabled',
        'image',
        'imageTag',
        'imagePullPolicy',
        'replicas',
        'concurrency',
        'resources',
        'persistence',
        'nodeSelector',
        'affinity',
        'tolerations'
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 resources=None,
                 persistence=None,
                 nodeSelector=None,
                 affinity=None,
                 tolerations=None):
        super(ThirdPartyServiceConfig, self).__init__(
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            resources=resources,
        )
        self.enabled = enabled
        self.persistence = persistence
        self.nodeSelector = nodeSelector
        self.affinity = affinity
        self.tolerations = tolerations


class PostgresqlSchema(ThirdPartyServiceSchema):
    postgresUser = fields.Str(allow_none=True)
    postgresPassword = fields.Str(allow_none=True)
    postgresDatabase = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return PostgresqlConfig


class PostgresqlConfig(ThirdPartyServiceConfig):
    SCHEMA = PostgresqlSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'postgresUser',
        'postgresPassword',
        'postgresDatabase',
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 postgresUser=None,
                 postgresPassword=None,
                 postgresDatabase=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 resources=None,
                 persistence=None,
                 nodeSelector=None,
                 affinity=None,
                 tolerations=None):
        super(PostgresqlConfig, self).__init__(
            enabled=enabled,
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            nodeSelector=nodeSelector,
            affinity=affinity,
            tolerations=tolerations, )
        self.postgresUser = postgresUser
        self.postgresPassword = postgresPassword
        self.postgresDatabase = postgresDatabase


class RedisSchema(ThirdPartyServiceSchema):
    image = fields.Raw(allow_none=True)
    usePassword = fields.Bool(allow_none=True)
    password = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RedisConfig


class RedisConfig(ThirdPartyServiceConfig):
    SCHEMA = RedisSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'usePassword',
        'password',
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 usePassword=None,
                 password=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 resources=None,
                 persistence=None,
                 nodeSelector=None,
                 affinity=None,
                 tolerations=None):
        super(RedisConfig, self).__init__(
            enabled=enabled,
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            nodeSelector=nodeSelector,
            affinity=affinity,
            tolerations=tolerations, )
        self.usePassword = usePassword
        self.password = password


class RabbitmqSchema(ThirdPartyServiceSchema):
    rabbitmqUsername = fields.Str(allow_none=True)
    rabbitmqPassword = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RabbitmqConfig


class RabbitmqConfig(ThirdPartyServiceConfig):
    SCHEMA = RabbitmqSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'rabbitmqUsername',
        'rabbitmqPassword',
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 rabbitmqUsername=None,
                 rabbitmqPassword=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 resources=None,
                 persistence=None,
                 nodeSelector=None,
                 affinity=None,
                 tolerations=None):
        super(RabbitmqConfig, self).__init__(
            enabled=enabled,
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            nodeSelector=nodeSelector,
            affinity=affinity,
            tolerations=tolerations, )
        self.rabbitmqUsername = rabbitmqUsername
        self.rabbitmqPassword = rabbitmqPassword


class DockerRegistrySchema(ThirdPartyServiceSchema):
    registryUser = fields.Str(allow_none=True)
    registryPassword = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return DockerRegistryConfig


class DockerRegistryConfig(ThirdPartyServiceConfig):
    SCHEMA = DockerRegistrySchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'registryUser',
        'registryPassword',
    ]

    def __init__(self,  # noqa
                 enabled=None,
                 registryUser=None,
                 registryPassword=None,
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 resources=None,
                 persistence=None,
                 nodeSelector=None,
                 affinity=None,
                 tolerations=None):
        super(DockerRegistryConfig, self).__init__(
            enabled=enabled,
            image=image,
            imageTag=imageTag,
            imagePullPolicy=imagePullPolicy,
            replicas=replicas,
            resources=resources,
            persistence=persistence,
            nodeSelector=nodeSelector,
            affinity=affinity,
            tolerations=tolerations, )
        self.registryUser = registryUser
        self.registryPassword = registryPassword


class ExternalServiceSchema(BaseSchema):
    user = fields.Str(allow_none=True)
    password = fields.Str(allow_none=True)
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    database = fields.Str(allow_none=True)
    usePassword = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return ExternalServiceConfig


class ExternalServiceConfig(BaseConfig):
    SCHEMA = ExternalServiceSchema
    REDUCED_ATTRIBUTES = [
        'user',
        'password',
        'host',
        'port',
        'database',
        'usePassword'
    ]

    def __init__(self,  # noqa
                 user=None,
                 password=None,
                 host=None,
                 port=None,
                 database=None,
                 usePassword=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.usePassword = usePassword


class ExternalServicesSchema(BaseSchema):
    redis = fields.Nested(ExternalServiceSchema, allow_none=True)
    rabbitmq = fields.Nested(ExternalServiceSchema, allow_none=True)
    postgresql = fields.Nested(ExternalServiceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ExternalServicesConfig


class ExternalServicesConfig(BaseConfig):
    SCHEMA = ExternalServicesSchema
    REDUCED_ATTRIBUTES = [
        'redis',
        'rabbitmq',
        'postgresql',
    ]

    def __init__(self,
                 redis=None,
                 rabbitmq=None,
                 postgresql=None):
        self.redis = redis
        self.rabbitmq = rabbitmq
        self.postgresql = postgresql
