# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema
from polyaxon_deploy.schemas.deployment_types import DeploymentTypes
from polyaxon_deploy.schemas.email import EmailSchema
from polyaxon_deploy.schemas.ingress import IngressSchema
from polyaxon_deploy.schemas.intervals import IntervalsSchema
from polyaxon_deploy.schemas.persistence import PersistenceSchema
from polyaxon_deploy.schemas.rbac import RBACSchema
from polyaxon_deploy.schemas.root_user import RootUserSchema
from polyaxon_deploy.schemas.security_context import SecurityContextSchema
from polyaxon_deploy.schemas.service import (
    ApiSchema,
    DockerRegistrySchema,
    EventMonitorsSchema,
    ExternalServicesSchema,
    HooksSchema,
    PostgresqlSchema,
    RabbitmqSchema,
    RedisSchema,
    ServiceSchema,
    ThirdPartyServiceSchema,
    WorkerSchema
)
from polyaxon_deploy.schemas.service_types import ServiceTypes
from polyaxon_deploy.schemas.ssl import SSLSchema


def check_redis(redis, external_services):
    redis_disabled = redis.enabled is False if redis else False
    external_redis = None
    if external_services:
        external_redis = external_services.redis

    if redis_disabled and not external_redis:
        raise ValidationError('A redis instance is required, please enable the in-cluster redis, '
                              'or provide an external instance.')


def check_postgres(postgresql, external_services):
    postgresql_disabled = postgresql.enabled is False if postgresql else False
    external_postgresql = None
    if external_services:
        external_postgresql = external_services.postgresql

    if postgresql_disabled and not external_postgresql:
        raise ValidationError('A postgresql instance is required, '
                              'please enable the in-cluster postgresql, '
                              'or provide an external instance.')


def check_rabbitmq(rabbitmq, external_services, broker):
    rabbitmq_disabled = rabbitmq.enabled is False if rabbitmq else False
    external_rabbitmq = None
    rabbitmq_borker = broker != 'redis'
    if external_services:
        external_rabbitmq = external_services.rabbitmq

    if rabbitmq_disabled and rabbitmq_borker and not external_rabbitmq:
        raise ValidationError('Rabbitmq is used as a broker, '
                              'an instance is required, '
                              'please enable the in-cluster rabbitmq, '
                              'or provide an external instance.')


class DeploymentSchema(BaseSchema):
    deploymentType = fields.Str(allow_none=True, validate=validate.OneOf(DeploymentTypes.VALUES))
    deploymentVersion = fields.Str(allow_none=True)
    clusterId = fields.Str(allow_none=True)
    namespace = fields.Str(allow_none=True)
    rbac = fields.Nested(RBACSchema, allow_none=True)
    polyaxonSecret = fields.Str(allow_none=True)
    internalToken = fields.Str(allow_none=True)
    passwordLength = fields.Int(allow_none=True)
    ssl = fields.Nested(SSLSchema, allow_none=True)
    encryptionSecret = fields.Str(allow_none=True)
    serviceType = fields.Str(allow_none=True, validate=validate.OneOf(ServiceTypes.VALUES))
    adminViewEnabled = fields.Bool(allow_none=True)
    timeZone = fields.Str(allow_none=True)
    environment = fields.Str(allow_none=True)
    ingress = fields.Nested(IngressSchema, allow_none=True)
    user = fields.Nested(RootUserSchema, allow_none=True)
    nodeSelector = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(allow_none=True), allow_none=True)
    affinity = fields.Dict(allow_none=True)
    limitResources = fields.Bool(allow_none=True)
    globalReplicas = fields.Int(allow_none=True)
    globalConcurrency = fields.Int(allow_none=True)
    api = fields.Nested(ApiSchema, allow_none=True)
    streams = fields.Nested(ApiSchema, allow_none=True)
    scheduler = fields.Nested(WorkerSchema, allow_none=True)
    worker = fields.Nested(WorkerSchema, allow_none=True)
    hpsearch = fields.Nested(WorkerSchema, allow_none=True)
    eventsHandlers = fields.Nested(WorkerSchema, allow_none=True)
    k8sEventsHandlers = fields.Nested(WorkerSchema, allow_none=True)
    beat = fields.Nested(ServiceSchema, allow_none=True)
    crons = fields.Nested(ServiceSchema, allow_none=True)
    eventMonitors = fields.Nested(EventMonitorsSchema, allow_none=True)
    resourcesDaemon = fields.Nested(ThirdPartyServiceSchema, allow_none=True)
    tablesHook = fields.Nested(ServiceSchema, allow_none=True)
    hooks = fields.Nested(HooksSchema, allow_none=True)
    postgresql = fields.Nested(PostgresqlSchema, allow_none=True)
    redis = fields.Nested(RedisSchema, allow_none=True)
    rabbitmq = fields.Nested(RabbitmqSchema,
                             data_key="rabbitmq-ha",
                             allow_none=True)
    broker = fields.Str(allow_none=True, validate=validate.OneOf(['redis', 'rabbitmq']))
    dockerRegistry = fields.Nested(DockerRegistrySchema,
                                   data_key="docker-registry",
                                   allow_none=True)
    email = fields.Nested(EmailSchema, allow_none=True)
    ldap = fields.Raw(allow_none=True)
    hostName = fields.Str(allow_none=True)
    allowedHosts = fields.List(fields.Str(), allow_none=True)
    intervals = fields.Nested(IntervalsSchema, allow_none=True)
    persistence = fields.Nested(PersistenceSchema, allow_none=True)
    adminModels = fields.List(fields.Str(allow_none=True), allow_none=True)
    reposAccessToken = fields.Str(allow_none=True)
    logLevel = fields.Str(allow_none=True)
    trackerBackend = fields.Str(allow_none=True)
    dirs = fields.Dict(allow_none=True)
    mountPaths = fields.Dict(allow_none=True)
    securityContext = fields.Nested(SecurityContextSchema, allow_none=True)
    externalServices = fields.Nested(ExternalServicesSchema, allow_none=True)
    debugMode = fields.Bool(allow_none=True)

    # Pending validation
    dns = fields.Raw(allow_none=True)
    plugins = fields.Raw(allow_none=True)

    @staticmethod
    def schema_config():
        return DeploymentConfig

    @validates_schema
    def validate_deployment(self, data):
        check_redis(data.get('redis'), data.get('externalServices'))
        check_postgres(data.get('postgresql'), data.get('externalServices'))
        check_rabbitmq(data.get('rabbitmq'), data.get('externalServices'), data.get('broker'))


class DeploymentConfig(BaseConfig):
    SCHEMA = DeploymentSchema

    def __init__(self,  # noqa
                 deploymentType=None,
                 deploymentVersion=None,
                 clusterId=None,
                 namespace=None,
                 rbac=None,
                 polyaxonSecret=None,
                 internalToken=None,
                 passwordLength=None,
                 ssl=None,
                 dns=None,
                 encryptionSecret=None,
                 serviceType=None,
                 adminViewEnabled=None,
                 timeZone=None,
                 environment=None,
                 ingress=None,
                 user=None,
                 nodeSelector=None,
                 tolerations=None,
                 affinity=None,
                 limitResources=None,
                 globalReplicas=None,
                 globalConcurrency=None,
                 api=None,
                 streams=None,
                 scheduler=None,
                 worker=None,
                 hpsearch=None,
                 eventsHandlers=None,
                 k8sEventsHandlers=None,
                 beat=None,
                 crons=None,
                 eventMonitors=None,
                 resourcesDaemon=None,
                 tablesHook=None,
                 hooks=None,
                 postgresql=None,
                 redis=None,
                 rabbitmq=None,
                 broker=None,
                 dockerRegistry=None,
                 email=None,
                 ldap=None,
                 hostName=None,
                 allowedHosts=None,
                 intervals=None,
                 persistence=None,
                 adminModels=None,
                 reposAccessToken=None,
                 logLevel=None,
                 trackerBackend=None,
                 dirs=None,
                 mountPaths=None,
                 securityContext=None,
                 externalServices=None,
                 debugMode=None,
                 plugins=None):
        check_redis(redis, externalServices)
        check_postgres(postgresql, externalServices)
        check_rabbitmq(rabbitmq, externalServices, broker)
        self.deploymentType = deploymentType
        self.deploymentVersion = deploymentVersion
        self.clusterId = clusterId
        self.namespace = namespace
        self.rbac = rbac
        self.polyaxonSecret = polyaxonSecret
        self.internalToken = internalToken
        self.passwordLength = passwordLength
        self.ssl = ssl
        self.dns = dns
        self.encryptionSecret = encryptionSecret
        self.serviceType = serviceType
        self.adminViewEnabled = adminViewEnabled
        self.timeZone = timeZone
        self.environment = environment
        self.ingress = ingress
        self.user = user
        self.nodeSelector = nodeSelector
        self.tolerations = tolerations
        self.affinity = affinity
        self.limitResources = limitResources
        self.globalReplicas = globalReplicas
        self.globalConcurrency = globalConcurrency
        self.api = api
        self.streams = streams
        self.scheduler = scheduler
        self.worker = worker
        self.hpsearch = hpsearch
        self.eventsHandlers = eventsHandlers
        self.k8sEventsHandlers = k8sEventsHandlers
        self.beat = beat
        self.crons = crons
        self.eventMonitors = eventMonitors
        self.resourcesDaemon = resourcesDaemon
        self.tablesHook = tablesHook
        self.hooks = hooks
        self.postgresql = postgresql
        self.redis = redis
        self.rabbitmq = rabbitmq
        self.broker = broker
        self.dockerRegistry = dockerRegistry
        self.email = email
        self.ldap = ldap
        self.hostName = hostName
        self.allowedHosts = allowedHosts
        self.intervals = intervals
        self.persistence = persistence
        self.adminModels = adminModels
        self.reposAccessToken = reposAccessToken
        self.logLevel = logLevel
        self.trackerBackend = trackerBackend
        self.dirs = dirs
        self.mountPaths = mountPaths
        self.securityContext = securityContext
        self.externalServices = externalServices
        self.debugMode = debugMode
        self.plugins = plugins
