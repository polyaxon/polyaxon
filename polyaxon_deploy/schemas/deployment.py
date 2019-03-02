# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate
from polyaxon_deploy.schemas.auth import AuthSchema
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema
from polyaxon_deploy.schemas.deployment_types import DeploymentTypes
from polyaxon_deploy.schemas.email import EmailSchema
from polyaxon_deploy.schemas.ingress import IngressSchema
from polyaxon_deploy.schemas.integrations import IntegrationsSchema
from polyaxon_deploy.schemas.intervals import CleaningIntervalsSchema, IntervalsSchema, TTLSchema
from polyaxon_deploy.schemas.persistence import PersistenceSchema
from polyaxon_deploy.schemas.rbac import RBACSchema
from polyaxon_deploy.schemas.root_user import RootUserSchema
from polyaxon_deploy.schemas.scheduling import (
    AffinitySchema,
    NodeSelectorsSchema,
    TolerationsSchema
)
from polyaxon_deploy.schemas.service import (
    DockerRegistrySchema,
    EventMonitorsSchema,
    HooksSchema,
    PostgresqlSchema,
    RabbitmqSchema,
    ServiceSchema
)
from polyaxon_deploy.schemas.service_types import ServiceTypes

from polyaxon_schemas.utils import DictOrStr


class DeploymentSchema(BaseSchema):
    deploymentType = fields.Str(allow_none=True, validate=validate.OneOf(DeploymentTypes.VALUES))
    deploymentVersion = fields.Str(allow_none=True)
    clusterId = fields.Str(allow_none=True)
    namespace = fields.Str(allow_none=True)
    rbac = fields.Nested(RBACSchema, allow_none=True)
    serviceType = fields.Str(allow_none=True, validate=validate.OneOf(ServiceTypes.VALUES))
    adminViewEnabled = fields.Bool(allow_none=True)
    timeZone = fields.Str(allow_none=True)
    environment = fields.Str(allow_none=True)
    ingress = fields.Nested(IngressSchema, allow_none=True)
    user = fields.Nested(RootUserSchema, allow_none=True)
    nodeSelectors = fields.Nested(NodeSelectorsSchema, allow_none=True)
    tolerations = fields.Nested(TolerationsSchema, allow_none=True)
    affinity = fields.Nested(AffinitySchema, allow_none=True)
    limitResources = fields.Bool(allow_none=True)
    globalReplicas = fields.Int(allow_none=True)
    globalConcurrency = fields.Int(allow_none=True)
    api = fields.Nested(ServiceSchema, allow_none=True)
    streams = fields.Nested(ServiceSchema, allow_none=True)
    scheduler = fields.Nested(ServiceSchema, allow_none=True)
    hpsearch = fields.Nested(ServiceSchema, allow_none=True)
    eventsHandlers = fields.Nested(ServiceSchema, allow_none=True)
    k8sEventsHandlers = fields.Nested(ServiceSchema, allow_none=True)
    beat = fields.Nested(ServiceSchema, allow_none=True)
    crons = fields.Nested(ServiceSchema, allow_none=True)
    eventMonitors = fields.Nested(EventMonitorsSchema, allow_none=True)
    resourcesDaemon = fields.Nested(ServiceSchema, allow_none=True)
    sidecar = fields.Nested(ServiceSchema, allow_none=True)
    init = fields.Nested(HooksSchema, allow_none=True)
    dockerizer = fields.Nested(ServiceSchema, allow_none=True)
    tablesHook = fields.Nested(ServiceSchema, allow_none=True)
    hooks = fields.Nested(HooksSchema, allow_none=True)
    postgresql = fields.Nested(PostgresqlSchema, allow_none=True)
    rabbitmq = fields.Nested(RabbitmqSchema, allow_none=True)
    dockerRegistry = fields.Nested(DockerRegistrySchema,
                                   attribute="docker-registry",
                                   allow_none=True)
    email = fields.Nested(EmailSchema, allow_none=True)
    auth = fields.Nested(AuthSchema, allow_none=True)
    integrations = fields.Nested(IntegrationsSchema, allow_none=True)
    apiHost = fields.Str(allow_none=True)
    allowedHosts = fields.List(fields.Str(), allow_none=True)
    secretRefs = fields.List(fields.Str(), allow_none=True)
    configmapRefs = fields.List(fields.Str(), allow_none=True)
    intervals = fields.Nested(IntervalsSchema, allow_none=True)
    cleaningIntervals = fields.Nested(CleaningIntervalsSchema, allow_none=True)
    ttl = fields.Nested(TTLSchema, allow_none=True)
    privateRegistries = fields.List(DictOrStr(allow_none=True), allow_none=True)
    persistence = fields.Nested(PersistenceSchema, allow_none=True)
    notebookBackend = fields.Str(allow_none=True)
    notebookDockerImage = fields.Str(allow_none=True)
    tensorboardDockerImage = fields.Str(allow_none=True)
    adminModels = fields.List(fields.Str(allow_none=True), allow_none=True)
    reposAccessToken = fields.Str(allow_none=True)
    tpuTensorflowVersion = fields.Str(allow_none=True)
    tpuResourceKey = fields.Str(allow_none=True)
    logLevel = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return DeploymentConfig


class DeploymentConfig(BaseConfig):
    SCHEMA = DeploymentSchema

    def __init__(self,  # noqa
                 deploymentType=None,
                 deploymentVersion=None,
                 clusterId=None,
                 namespace=None,
                 rbac=None,
                 serviceType=None,
                 adminViewEnabled=None,
                 timeZone=None,
                 environment=None,
                 ingress=None,
                 user=None,
                 nodeSelectors=None,
                 tolerations=None,
                 affinity=None,
                 limitResources=None,
                 globalReplicas=None,
                 globalConcurrency=None,
                 api=None,
                 streams=None,
                 scheduler=None,
                 hpsearch=None,
                 eventsHandlers=None,
                 k8sEventsHandlers=None,
                 beat=None,
                 crons=None,
                 eventMonitors=None,
                 resourcesDaemon=None,
                 sidecar=None,
                 init=None,
                 dockerizer=None,
                 tablesHook=None,
                 hooks=None,
                 postgresql=None,
                 rabbitmq=None,
                 dockerRegistry=None,
                 email=None,
                 auth=None,
                 integrations=None,
                 apiHost=None,
                 allowedHosts=None,
                 secretRefs=None,
                 configmapRefs=None,
                 intervals=None,
                 cleaningIntervals=None,
                 ttl=None,
                 privateRegistries=None,
                 persistence=None,
                 notebookBackend=None,
                 notebookDockerImage=None,
                 tensorboardDockerImage=None,
                 adminModels=None,
                 reposAccessToken=None,
                 tpuTensorflowVersion=None,
                 tpuResourceKey=None,
                 logLevel=None):
        self.deploymentType = deploymentType
        self.deploymentVersion = deploymentVersion
        self.clusterId = clusterId
        self.namespace = namespace
        self.rbac = rbac
        self.serviceType = serviceType
        self.adminViewEnabled = adminViewEnabled
        self.timeZone = timeZone
        self.environment = environment
        self.ingress = ingress
        self.user = user
        self.nodeSelectors = nodeSelectors
        self.tolerations = tolerations
        self.affinity = affinity
        self.limitResources = limitResources
        self.globalReplicas = globalReplicas
        self.globalConcurrency = globalConcurrency
        self.api = api
        self.streams = streams
        self.scheduler = scheduler
        self.hpsearch = hpsearch
        self.eventsHandlers = eventsHandlers
        self.k8sEventsHandlers = k8sEventsHandlers
        self.beat = beat
        self.crons = crons
        self.eventMonitors = eventMonitors
        self.resourcesDaemon = resourcesDaemon
        self.sidecar = sidecar
        self.init = init
        self.dockerizer = dockerizer
        self.tablesHook = tablesHook
        self.hooks = hooks
        self.postgresql = postgresql
        self.rabbitmq = rabbitmq
        self.dockerRegistry = dockerRegistry
        self.email = email
        self.auth = auth
        self.integrations = integrations
        self.apiHost = apiHost
        self.allowedHosts = allowedHosts
        self.secretRefs = secretRefs
        self.configmapRefs = configmapRefs
        self.intervals = intervals
        self.cleaningIntervals = cleaningIntervals
        self.ttl = ttl
        self.privateRegistries = privateRegistries
        self.persistence = persistence
        self.notebookBackend = notebookBackend
        self.notebookDockerImage = notebookDockerImage
        self.tensorboardDockerImage = tensorboardDockerImage
        self.adminModels = adminModels
        self.reposAccessToken = reposAccessToken
        self.tpuTensorflowVersion = tpuTensorflowVersion
        self.tpuResourceKey = tpuResourceKey
        self.logLevel = logLevel
