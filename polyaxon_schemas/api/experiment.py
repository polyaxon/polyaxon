# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.humanize import humanize_timedelta
from marshmallow import fields, validate

from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.fields import UUID
from polyaxon_schemas.ops.environments.resources import PodResourcesSchema


class ExperimentJobSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    uuid = UUID()
    unique_name = fields.Str(allow_none=True)
    pod_id = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)
    experiment = fields.Int()
    experiment_name = fields.Str()
    last_status = fields.Str(allow_none=True)
    created_at = fields.LocalDateTime()
    updated_at = fields.LocalDateTime()
    started_at = fields.LocalDateTime(allow_none=True)
    finished_at = fields.LocalDateTime(allow_none=True)
    total_run = fields.Str(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    definition = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentJobConfig


class ExperimentJobConfig(BaseConfig):
    SCHEMA = ExperimentJobSchema
    IDENTIFIER = 'ExperimentJob'
    DEFAULT_EXCLUDE_ATTRIBUTES = [
        'uuid', 'definition', 'experiment', 'unique_name', 'updated_at', 'resources']
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at', 'started_at', 'finished_at']

    def __init__(self,
                 uuid,
                 experiment,
                 created_at,
                 updated_at,
                 definition=None,
                 unique_name=None,
                 pod_id=None,
                 id=None,  # pylint:disable=redefined-builtin
                 role=None,
                 last_status=None,
                 started_at=None,
                 finished_at=None,
                 resources=None,
                 total_run=None):
        self.uuid = uuid
        self.unique_name = unique_name
        self.pod_id = pod_id
        self.id = id
        self.role = role
        self.experiment = experiment
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.started_at = self.localize_date(started_at)
        self.finished_at = self.localize_date(finished_at)
        self.definition = definition
        self.last_status = last_status
        self.resources = resources
        self.total_run = total_run
        if all([self.started_at, self.finished_at]):
            self.total_run = humanize_timedelta((self.finished_at - self.started_at).seconds)


class ExperimentSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    uuid = UUID(allow_none=True)
    unique_name = fields.Str(allow_none=True)
    user = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    project = fields.Str(allow_none=True)
    experiment_group = fields.Str(allow_none=True)
    build_job = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    last_status = fields.Str(allow_none=True)
    last_metric = fields.Dict(allow_none=True)
    backend = fields.Str(allow_none=True)
    framework = fields.Str(allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    started_at = fields.LocalDateTime(allow_none=True)
    finished_at = fields.LocalDateTime(allow_none=True)
    total_run = fields.Str(allow_none=True)
    is_clone = fields.Bool(allow_none=True)
    has_tensorboard = fields.Bool(allow_none=True)
    content = fields.Str(allow_none=True)
    num_jobs = fields.Int(allow_none=True)
    params = fields.Dict(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    run_env = fields.Dict(allow_none=True)
    is_managed = fields.Bool(allow_none=True)
    ttl = fields.Int(allow_none=True)
    jobs = fields.Nested(ExperimentJobSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentConfig


class ExperimentConfig(BaseConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'Experiment'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'id', 'unique_name', 'user', 'experiment_group', 'build_job', 'last_status',
        'created_at', 'started_at', 'finished_at', 'total_run'
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at', 'started_at', 'finished_at']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 project=None,
                 experiment_group=None,
                 build_job=None,
                 description=None,
                 last_status=None,
                 last_metric=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 has_tensorboard=False,
                 content=None,
                 num_jobs=0,
                 params=None,
                 tags=None,
                 resources=None,
                 is_managed=None,
                 run_env=None,
                 jobs=None,
                 ttl=None,
                 backend=None,
                 framework=None,
                 total_run=None):
        self.id = id
        self.user = user
        self.uuid = uuid
        self.name = name
        self.unique_name = unique_name
        self.project = project
        self.experiment_group = experiment_group
        self.build_job = build_job
        self.description = description
        self.last_status = last_status
        self.last_metric = last_metric
        self.started_at = self.localize_date(started_at)
        self.finished_at = self.localize_date(finished_at)
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.is_clone = is_clone
        self.has_tensorboard = has_tensorboard
        self.content = content
        self.num_jobs = num_jobs
        self.params = params
        self.tags = tags
        self.resources = resources
        self.is_managed = is_managed
        self.run_env = run_env
        self.jobs = jobs
        self.ttl = ttl
        self.backend = backend
        self.framework = framework
        self.total_run = None
        if all([self.started_at, self.finished_at]):
            self.total_run = humanize_timedelta((self.finished_at - self.started_at).seconds)


class ExperimentStatusSchema(BaseSchema):
    id = fields.Int()
    uuid = UUID()
    experiment = fields.Int()
    created_at = fields.LocalDateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    traceback = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentStatusConfig


class ExperimentStatusConfig(BaseConfig):
    SCHEMA = ExperimentStatusSchema
    IDENTIFIER = 'ExperimentStatus'
    DATETIME_ATTRIBUTES = ['created_at']
    DEFAULT_EXCLUDE_ATTRIBUTES = ['experiment', 'uuid', 'traceback']

    def __init__(self,
                 id,  # pylint:disable=redefined-builtin
                 uuid,
                 experiment,
                 created_at,
                 status,
                 message=None,
                 traceback=None):
        self.id = id
        self.uuid = uuid
        self.experiment = experiment
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.traceback = traceback


class ExperimentMetricSchema(BaseSchema):
    id = fields.Int()
    uuid = UUID()
    experiment = fields.Int()
    created_at = fields.LocalDateTime()
    values = fields.Dict()

    @staticmethod
    def schema_config():
        return ExperimentMetricConfig


class ExperimentMetricConfig(BaseConfig):
    SCHEMA = ExperimentMetricSchema
    IDENTIFIER = 'ExperimentMetric'
    DATETIME_ATTRIBUTES = ['created_at']
    DEFAULT_EXCLUDE_ATTRIBUTES = ['experiment', 'uuid']

    def __init__(self,
                 id,  # pylint:disable=redefined-builtin
                 uuid,
                 experiment,
                 created_at,
                 values):
        self.id = id
        self.uuid = uuid
        self.experiment = experiment
        self.created_at = self.localize_date(created_at)
        self.values = values


class ExperimentJobStatusSchema(BaseSchema):
    id = fields.Int()
    uuid = UUID()
    job = fields.Int()
    created_at = fields.LocalDateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    details = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentJobStatusConfig


class ExperimentJobStatusConfig(BaseConfig):
    SCHEMA = ExperimentJobStatusSchema
    IDENTIFIER = 'ExperimentJobStatus'
    DEFAULT_EXCLUDE_ATTRIBUTES = ['job', 'details', 'uuid']
    DATETIME_ATTRIBUTES = ['created_at']

    def __init__(self,
                 id,  # pylint:disable=redefined-builtin
                 uuid,
                 job,
                 created_at,
                 status,
                 message=None,
                 details=None):
        self.id = id
        self.uuid = uuid
        self.job = job
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.details = details


class ContainerGPUResourcesSchema(BaseSchema):
    index = fields.Int()
    uuid = fields.Str()
    name = fields.Str()
    minor = fields.Int()
    bus_id = fields.Str()
    serial = fields.Str()
    temperature_gpu = fields.Int()
    utilization_gpu = fields.Int()
    power_draw = fields.Int()
    power_limit = fields.Int()
    memory_free = fields.Int()
    memory_used = fields.Int()
    memory_total = fields.Int()
    memory_utilization = fields.Int()
    processes = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerGPUResourcesConfig


class ContainerGPUResourcesConfig(BaseConfig):
    SCHEMA = ContainerGPUResourcesSchema
    IDENTIFIER = 'ContainerGPUResources'
    MEM_SIZE_ATTRIBUTES = ['memory_free', 'memory_used', 'memory_total']

    def __init__(self,
                 index,
                 uuid,
                 name,
                 minor,
                 bus_id,
                 serial,
                 temperature_gpu,
                 utilization_gpu,
                 power_draw,
                 power_limit,
                 memory_free,
                 memory_used,
                 memory_total,
                 memory_utilization,
                 processes=None):
        self.index = index
        self.uuid = uuid
        self.name = name
        self.minor = minor
        self.bus_id = bus_id
        self.serial = serial
        self.temperature_gpu = temperature_gpu
        self.utilization_gpu = utilization_gpu
        self.power_draw = power_draw
        self.power_limit = power_limit
        self.memory_free = memory_free
        self.memory_used = memory_used
        self.memory_total = memory_total
        self.memory_utilization = memory_utilization
        self.processes = processes


class ContainerResourcesSchema(BaseSchema):
    job_uuid = UUID()
    experiment_uuid = UUID()
    job_name = fields.Str()
    container_id = fields.Str()
    n_cpus = fields.Int()
    cpu_percentage = fields.Float()
    percpu_percentage = fields.List(fields.Float(), allow_none=True)
    memory_used = fields.Int()
    memory_limit = fields.Int()
    gpu_resources = fields.Nested(ContainerGPUResourcesSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerResourcesConfig


class ContainerResourcesConfig(BaseConfig):
    SCHEMA = ContainerResourcesSchema
    IDENTIFIER = 'ContainerResources'
    PERCENT_ATTRIBUTES = ['cpu_percentage']
    MEM_SIZE_ATTRIBUTES = ['memory_used', 'memory_limit']

    def __init__(self,
                 job_uuid,
                 experiment_uuid,
                 job_name,
                 container_id,
                 n_cpus,
                 cpu_percentage,
                 percpu_percentage,
                 memory_used,
                 memory_limit,
                 gpu_resources=None):
        self.job_uuid = job_uuid
        self.experiment_uuid = experiment_uuid
        self.job_name = job_name
        self.container_id = container_id
        self.n_cpus = n_cpus
        self.cpu_percentage = cpu_percentage
        self.percpu_percentage = percpu_percentage
        self.memory_used = memory_used
        self.memory_limit = memory_limit
        self.gpu_resources = gpu_resources
