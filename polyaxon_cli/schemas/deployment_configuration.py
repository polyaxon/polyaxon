# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_cli.schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.environments import K8SContainerResourcesSchema
from polyaxon_schemas.utils import DictOrStr


class ServiceTypes(object):
    LOAD_BALANCER = 'LoadBalancer'
    NODE_PORT = 'NodePort'
    CLUSTER_IP = 'clusterIP'

    VALUES = [LOAD_BALANCER, NODE_PORT, CLUSTER_IP]


class DeploymentTypes(object):
    KUBERNETES = 'kubernetes'
    DOCKER_COMPOSE = 'docker-compose'
    DOCKER = 'docker'
    HEROKU = 'heroku'

    VALUES = [KUBERNETES, DOCKER_COMPOSE, DOCKER, HEROKU]


class RBACSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return RBACConfig


class RBACConfig(BaseConfig):
    SCHEMA = RBACSchema
    REDUCED_ATTRIBUTES = ['enabled']

    def __init__(self, enabled=None):
        self.enabled = enabled


class IngressSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    tls = fields.Dict(allow_none=True)
    annotations = fields.Dict(allow_none=True)
    resources = fields.Nested(K8SContainerResourcesSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return IngressConfig


class IngressConfig(BaseConfig):
    SCHEMA = IngressSchema
    REDUCED_ATTRIBUTES = ['enabled', 'tls', 'annotations', 'resources']

    def __init__(self,
                 enabled=None,
                 tls=None,
                 annotations=None,
                 resources=None):
        self.enabled = enabled
        self.tls = tls
        self.annotations = annotations
        self.resources = resources


class RootUserSchema(BaseSchema):
    username = fields.Str(allow_none=True, default='root')
    password = fields.Str(allow_none=True, default='rootpassword')
    email = fields.Email(allow_none=True)

    @staticmethod
    def schema_config():
        return RootUserConfig


class RootUserConfig(BaseConfig):
    SCHEMA = RootUserSchema
    REDUCED_ATTRIBUTES = ['username', 'password', 'email']

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email


class NodeSelectorsSchema(BaseSchema):
    core = fields.Dict(allow_none=True)
    experiments = fields.Dict(allow_none=True)
    jobs = fields.Dict(allow_none=True)
    builds = fields.Dict(allow_none=True)
    tensorboards = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return NodeSelectorsConfig


class NodeSelectorsConfig(BaseConfig):
    SCHEMA = NodeSelectorsSchema
    REDUCED_ATTRIBUTES = ['core', 'experiments', 'jobs', 'builds', 'tensorboards']

    def __init__(self,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards


class AffinitySchema(BaseSchema):
    core = fields.Dict(allow_none=True)
    experiments = fields.Dict(allow_none=True)
    jobs = fields.Dict(allow_none=True)
    builds = fields.Dict(allow_none=True)
    tensorboards = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return AffinityConfig


class AffinityConfig(BaseConfig):
    SCHEMA = AffinitySchema
    REDUCED_ATTRIBUTES = ['core', 'experiments', 'jobs', 'builds', 'tensorboards']

    def __init__(self,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards


class TolerationsSchema(BaseSchema):
    resourcesDaemon = fields.List(fields.Dict(allow_none=True), allow_none=True)
    core = fields.List(fields.Dict(allow_none=True), allow_none=True)
    experiments = fields.List(fields.Dict(allow_none=True), allow_none=True)
    jobs = fields.List(fields.Dict(allow_none=True), allow_none=True)
    builds = fields.List(fields.Dict(allow_none=True), allow_none=True)
    tensorboards = fields.List(fields.Dict(allow_none=True), allow_none=True)

    @staticmethod
    def schema_config():
        return TolerationsConfig


class TolerationsConfig(BaseConfig):
    SCHEMA = TolerationsSchema
    REDUCED_ATTRIBUTES = [
        'resourcesDaemon',
        'core',
        'experiments',
        'jobs',
        'builds',
        'tensorboards'
    ]

    def __init__(self,  # noqa
                 resourcesDaemon=None,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.resourcesDaemon = resourcesDaemon
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards


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


class EmailSchema(BaseSchema):
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    useTls = fields.Bool(allow_none=True)
    hostUser = fields.Str(allow_none=True)
    hostPassword = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return EmailConfig


class EmailConfig(BaseConfig):
    SCHEMA = EmailSchema
    REDUCED_ATTRIBUTES = ['host', 'port', 'useTls', 'hostUser', 'hostPassword']

    def __init__(self, host=None, port=None, useTls=None, hostUser=None, hostPassword=None):  # noqa
        self.host = host
        self.port = port
        self.useTls = useTls
        self.hostUser = hostUser
        self.hostPassword = hostPassword


class IntegrationsSchema(BaseSchema):
    slack = fields.List(fields.Dict(), allow_none=True)
    hipchat = fields.List(fields.Dict(), allow_none=True)
    mattermost = fields.List(fields.Dict(), allow_none=True)
    discord = fields.List(fields.Dict(), allow_none=True)
    pagerduty = fields.List(fields.Dict(), allow_none=True)
    webhooks = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return IntegrationsConfig


class IntegrationsConfig(BaseConfig):
    SCHEMA = IntegrationsSchema
    REDUCED_ATTRIBUTES = ['slack', 'hipchat', 'mattermost', 'discord', 'pagerduty', 'webhooks']

    def __init__(self,
                 slack=None,
                 hipchat=None,
                 mattermost=None,
                 discord=None,
                 pagerduty=None,
                 webhooks=None):
        self.slack = slack
        self.hipchat = hipchat
        self.mattermost = mattermost
        self.discord = discord
        self.pagerduty = pagerduty
        self.webhooks = webhooks


class IntervalsSchema(BaseSchema):
    experimentsScheduler = fields.Int(default=None)
    experimentsSync = fields.Int(default=None)
    clustersUpdateSystemInfo = fields.Int(default=None)
    clustersUpdateSystemNodes = fields.Int(default=None)
    pipelinesScheduler = fields.Int(default=None)
    operationsDefaultRetryDelay = fields.Int(default=None)
    operationsMaxRetryDelay = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return IntervalsConfig


class IntervalsConfig(BaseConfig):
    SCHEMA = IntervalsSchema
    REDUCED_ATTRIBUTES = [
        'experimentsScheduler',
        'experimentsSync',
        'clustersUpdateSystemInfo',
        'clustersUpdateSystemNodes',
        'pipelinesScheduler',
        'operationsDefaultRetryDelay',
        'operationsMaxRetryDelay',
    ]

    def __init__(self,  # noqa
                 experimentsScheduler=None,
                 experimentsSync=None,
                 clustersUpdateSystemInfo=None,
                 clustersUpdateSystemNodes=None,
                 pipelinesScheduler=None,
                 operationsDefaultRetryDelay=None,
                 operationsMaxRetryDelay=None):
        self.experimentsScheduler = experimentsScheduler
        self.experimentsSync = experimentsSync
        self.clustersUpdateSystemInfo = clustersUpdateSystemInfo
        self.clustersUpdateSystemNodes = clustersUpdateSystemNodes
        self.pipelinesScheduler = pipelinesScheduler
        self.operationsDefaultRetryDelay = operationsDefaultRetryDelay
        self.operationsMaxRetryDelay = operationsMaxRetryDelay


class CleaningIntervalsSchema(BaseSchema):
    archived = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return CleaningIntervalsConfig


class CleaningIntervalsConfig(BaseConfig):
    SCHEMA = CleaningIntervalsSchema
    REDUCED_ATTRIBUTES = ['archived']

    def __init__(self, archived=None):
        self.archived = archived


class TTLSchema(BaseSchema):
    token = fields.Int(allow_none=True)
    ephemeralToken = fields.Int(allow_none=True)
    heartbeat = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return TTLConfig


class TTLConfig(BaseConfig):
    SCHEMA = TTLSchema
    REDUCED_ATTRIBUTES = ['token', 'ephemeralToken', 'heartbeat']

    def __init__(self, token=None, ephemeralToken=None, heartbeat=None):  # noqa
        self.token = token
        self.ephemeralToken = ephemeralToken
        self.heartbeat = heartbeat


class PersistenceEntitySchema(BaseSchema):
    existingClaim = fields.Str(allow_none=True)
    mountPath = fields.Str(allow_none=True)
    hostPath = fields.Str(allow_none=True)
    store = fields.Str(allow_none=True)
    bucket = fields.Str(allow_none=True)
    secret = fields.Str(allow_none=True)
    secretKey = fields.Str(allow_none=True)
    readOnly = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceEntityConfig


class PersistenceEntityConfig(BaseConfig):
    SCHEMA = PersistenceEntitySchema
    REDUCED_ATTRIBUTES = [
        'existingClaim',
        'mountPath',
        'hostPath',
        'store',
        'bucket',
        'secret',
        'secretKey',
        'readOnly'
    ]

    def __init__(self,  # noqa
                 existingClaim=None,
                 mountPath=None,
                 hostPath=None,
                 store=None,
                 bucket=None,
                 secret=None,
                 secretKey=None,
                 readOnly=None):
        self.existingClaim = existingClaim
        self.mountPath = mountPath
        self.hostPath = hostPath
        self.store = store
        self.bucket = bucket
        self.secret = secret
        self.secretKey = secretKey
        self.readOnly = readOnly


def validate_named_persistence(values, persistence):
    if not values:
        return
    for key, value in six.iteritems(values):
        try:
            PersistenceEntityConfig.from_dict(value)
        except (KeyError, ValidationError):
            raise ValidationError(
                "Persistence name `{}` under `{}` is not valid.".format(key, persistence))


class PersistenceSchema(BaseSchema):
    logs = fields.Nested(PersistenceEntitySchema, allow_none=True)
    repos = fields.Nested(PersistenceEntitySchema, allow_none=True)
    upload = fields.Nested(PersistenceEntitySchema, allow_none=True)
    data = fields.Dict(allow_none=True)
    outputs = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceConfig

    @validates_schema
    def validate_quantity(self, data):
        validate_named_persistence(data.get('data'), 'data')
        validate_named_persistence(data.get('outputs'), 'outputs')


class PersistenceConfig(BaseConfig):
    SCHEMA = PersistenceSchema
    REDUCED_ATTRIBUTES = ['logs', 'repos', 'upload', 'data', 'outputs']

    def __init__(self, logs=None, repos=None, upload=None, data=None, outputs=None):
        self.logs = logs
        self.repos = repos
        self.upload = upload
        if data:
            validate_named_persistence(data, 'data')
        self.data = data
        if outputs:
            validate_named_persistence(outputs, 'outputs')
        self.outputs = outputs


class DeploymentSchema(BaseSchema):
    deploymentType = fields.Str(allow_none=True, validate=validate.OneOf(DeploymentTypes.VALUES))
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
    reourcesDaemon = fields.Nested(ServiceSchema, allow_none=True)
    sidecar = fields.Nested(ServiceSchema, allow_none=True)
    dockerizer = fields.Nested(ServiceSchema, allow_none=True)
    hooks = fields.Nested(ServiceSchema, allow_none=True)
    postgresql = fields.Nested(PostgresqlSchema, allow_none=True)
    rabbitmq = fields.Nested(RabbitmqSchema, allow_none=True)
    dockerRegistry = fields.Nested(DockerRegistrySchema,
                                   attribute="docker-registry",
                                   allow_none=True)
    email = fields.Nested(EmailSchema, allow_none=True)
    integrations = fields.Nested(IntegrationsSchema, allow_none=True)
    apiHost = fields.Str(allow_none=True)
    allowedHosts = fields.Str(allow_none=True, many=True)
    secretRefs = fields.Str(allow_none=True, many=True)
    configmapRefs = fields.Str(allow_none=True, many=True)
    intervals = fields.Nested(IntervalsSchema, allow_none=True)
    cleaningIntervals = fields.Nested(CleaningIntervalsSchema, allow_none=True)
    ttl = fields.Nested(TTLSchema, allow_none=True)
    privateRegistries = fields.List(DictOrStr(allow_none=True), allow_none=True)
    persistence = fields.Nested(PersistenceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return DeploymentConfig


class DeploymentConfig(BaseConfig):
    SCHEMA = DeploymentSchema

    def __init__(self,  # noqa
                 deploymentType=None,
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
                 reourcesDaemon=None,
                 sidecar=None,
                 dockerizer=None,
                 hooks=None,
                 postgresql=None,
                 rabbitmq=None,
                 dockerRegistry=None,
                 email=None,
                 integrations=None,
                 apiHost=None,
                 allowedHosts=None,
                 secretRefs=None,
                 configmapRefs=None,
                 intervals=None,
                 cleaningIntervals=None,
                 ttl=None,
                 privateRegistries=None,
                 persistence=None):
        self.deploymentType = deploymentType
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
        self.reourcesDaemon = reourcesDaemon
        self.sidecar = sidecar
        self.dockerizer = dockerizer
        self.hooks = hooks
        self.postgresql = postgresql
        self.rabbitmq = rabbitmq
        self.dockerRegistry = dockerRegistry
        self.email = email
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
