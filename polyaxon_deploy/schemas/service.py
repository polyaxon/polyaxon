# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema

from polyaxon_schemas.environments import K8SContainerResourcesSchema


class ServiceSchema(BaseSchema):
    image = fields.Str(allow_none=True)
    imageTag = fields.Str(allow_none=True)
    imagePullPolicy = fields.Str(allow_none=True)
    replicas = fields.Int(allow_none=True)
    concurrency = fields.Int(allow_none=True)
    resources = fields.Nested(K8SContainerResourcesSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ServiceConfig


class ServiceConfig(BaseConfig):
    SCHEMA = ServiceSchema
    REDUCED_ATTRIBUTES = [
        'image',
        'imageTag',
        'imagePullPolicy',
        'replicas',
        'concurrency',
        'resources'
    ]

    def __init__(self,  # noqa
                 image=None,
                 imageTag=None,
                 imagePullPolicy=None,
                 replicas=None,
                 concurrency=None,
                 resources=None):
        self.image = image
        self.imageTag = imageTag
        self.imagePullPolicy = imagePullPolicy
        self.replicas = replicas
        self.concurrency = concurrency
        self.resources = resources


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


class ThirdPartyServiceSchema(ServiceSchema):
    install = fields.Bool(allow_none=True)
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
        'install',
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
                 install=None,
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
        self.install = install
        self.persistence = persistence
        self.nodeSelector = nodeSelector
        self.affinity = affinity
        self.tolerations = tolerations


class PostgresqlSchema(ThirdPartyServiceSchema):
    postgresUser = fields.Str(allow_none=True)
    postgresPassword = fields.Str(allow_none=True)
    postgresDatabase = fields.Str(allow_none=True)
    externalPostgresHost = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return PostgresqlConfig


class PostgresqlConfig(ThirdPartyServiceConfig):
    SCHEMA = PostgresqlSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'postgresUser',
        'postgresPassword',
        'postgresDatabase',
        'externalPostgresHost'
    ]

    def __init__(self,  # noqa
                 install=None,
                 postgresUser=None,
                 postgresPassword=None,
                 postgresDatabase=None,
                 externalPostgresHost=None,
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
            install=install,
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
        self.externalPostgresHost = externalPostgresHost


class RedisSchema(ThirdPartyServiceSchema):
    usePassword = fields.Bool(allow_none=True)
    redisPassword = fields.Str(allow_none=True)
    externalRedisHost = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RedisConfig


class RedisConfig(ThirdPartyServiceConfig):
    SCHEMA = RedisSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'usePassword',
        'redisPassword',
        'externalRedisHost',
    ]

    def __init__(self,  # noqa
                 install=None,
                 usePassword=None,
                 redisPassword=None,
                 externalRedisHost=None,
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
            install=install,
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
        self.redisPassword = redisPassword
        self.externalRedisHost = externalRedisHost


class RabbitmqSchema(ThirdPartyServiceSchema):
    rabbitmqUsername = fields.Str(allow_none=True)
    rabbitmqPassword = fields.Str(allow_none=True)
    externalRabbitmqHost = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RabbitmqConfig


class RabbitmqConfig(ThirdPartyServiceConfig):
    SCHEMA = RabbitmqSchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'rabbitmqUsername',
        'rabbitmqPassword',
        'externalRabbitmqHost',
    ]

    def __init__(self,  # noqa
                 install=None,
                 rabbitmqUsername=None,
                 rabbitmqPassword=None,
                 externalRabbitmqHost=None,
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
            install=install,
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
        self.externalRabbitmqHost = externalRabbitmqHost


class DockerRegistrySchema(ThirdPartyServiceSchema):
    registryUser = fields.Str(allow_none=True)
    registryPassword = fields.Str(allow_none=True)
    externalRegistryHost = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return DockerRegistryConfig


class DockerRegistryConfig(ThirdPartyServiceConfig):
    SCHEMA = DockerRegistrySchema
    REDUCED_ATTRIBUTES = ThirdPartyServiceConfig.REDUCED_ATTRIBUTES + [
        'registryUser',
        'registryPassword',
        'externalRegistryHost',
    ]

    def __init__(self,  # noqa
                 install=None,
                 registryUser=None,
                 registryPassword=None,
                 externalRegistryHost=None,
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
            install=install,
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
        self.externalRegistryHost = externalRegistryHost
