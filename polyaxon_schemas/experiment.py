# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import UUID


class ExperimentJobSchema(Schema):
    uuid = UUID()
    experiment = UUID()
    created_at = fields.DateTime()
    definition = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentJobConfig(**data)

    @post_dump
    def unmake(self, data):
        return ExperimentJobConfig.remove_reduced_attrs(data)


class ExperimentJobConfig(BaseConfig):
    SCHEMA = ExperimentJobSchema
    IDENTIFIER = 'ExperimentJob'

    def __init__(self, uuid, experiment, created_at, definition):
        self.uuid = uuid
        self.experiment = experiment
        self.created_at = self.localize_date(created_at)
        self.definition = definition


class ExperimentSchema(Schema):
    name = fields.Str()
    uuid = UUID(allow_none=True)
    project = UUID(allow_none=True)
    group = UUID(allow_none=True)
    description = fields.Str(allow_none=True)
    config = fields.Dict(allow_none=True)
    content = fields.Str(allow_none=True)
    jobs = fields.Nested(ExperimentJobSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentConfig(**data)

    @post_dump
    def unmake(self, data):
        return ExperimentConfig.remove_reduced_attrs(data)


class ExperimentConfig(BaseConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'Experiment'
    REDUCED_ATTRIBUTES = ['description', 'group', 'jobs', 'content']

    def __init__(self,
                 name,
                 config=None,
                 content=None,
                 uuid=None,
                 project=None,
                 group=None,
                 jobs=None,
                 description=None):
        self.name = name
        self.config = config  # The json compiled content of this experiment
        self.content = content  # The yaml content when the experiment is independent
        self.uuid = uuid
        self.project = project
        self.group = group
        self.jobs = jobs
        self.description = description


class ExperimentStatusSchema(Schema):
    uuid = UUID()
    experiment = UUID()
    created_at = fields.DateTime()
    status = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentStatusConfig(**data)

    @post_dump
    def unmake(self, data):
        return ExperimentStatusConfig.remove_reduced_attrs(data)


class ExperimentStatusConfig(BaseConfig):
    SCHEMA = ExperimentStatusSchema
    IDENTIFIER = 'ExperimentStatus'

    def __init__(self, uuid, experiment, created_at, status):
        self.uuid = uuid
        self.experiment = experiment
        self.created_at = self.localize_date(created_at)
        self.status = status


class ExperimentJobStatusSchema(Schema):
    uuid = UUID()
    job = UUID()
    created_at = fields.DateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    details = fields.Dict(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentJobStatusConfig(**data)

    @post_dump
    def unmake(self, data):
        return ExperimentJobStatusConfig.remove_reduced_attrs(data)


class ExperimentJobStatusConfig(BaseConfig):
    SCHEMA = ExperimentJobStatusSchema
    IDENTIFIER = 'ExperimentJobStatus'
    REDUCED_ATTRIBUTES = ['message', 'details']

    def __init__(self, uuid, job, created_at, status, message=None, details=None):
        self.uuid = uuid
        self.job = job
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.details = details


class JobLabelSchema(Schema):
    project = fields.Str()
    experiment = fields.Str()
    task_type = fields.Str()
    task_idx = fields.Str()
    task = fields.Str()
    job_id = fields.Str()
    role = fields.Str()
    type = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return JobLabelConfig(**data)

    @post_dump
    def unmake(self, data):
        return JobLabelConfig.remove_reduced_attrs(data)


class JobLabelConfig(BaseConfig):
    SCHEMA = JobLabelSchema
    IDENTIFIER = 'JobLabel'

    def __init__(self, project, experiment, task_type, task_idx, task, job_id, role, type):
        self.project = project
        self.experiment = experiment
        self.task_type = task_type
        self.task_idx = task_idx
        self.task = task
        self.job_id = job_id
        self.role = role
        self.type = type


class PodStateSchema(Schema):
    event_type = fields.Str()
    labels = fields.Nested(JobLabelSchema)
    phase = fields.Str()
    deletion_timestamp = fields.DateTime(allow_none=True)
    pod_conditions = fields.Dict(allow_none=True)
    container_statuses = fields.Dict(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PodStateConfig(**data)

    @post_dump
    def unmake(self, data):
        return PodStateConfig.remove_reduced_attrs(data)


class PodStateConfig(BaseConfig):
    SCHEMA = PodStateSchema
    IDENTIFIER = 'PodState'

    def __init__(self,
                 event_type,
                 labels,
                 phase,
                 deletion_timestamp=None,
                 pod_conditions=None,
                 container_statuses=None):
        self.event_type = event_type
        self.labels = labels
        self.phase = phase
        self.deletion_timestamp = deletion_timestamp
        self.pod_conditions = pod_conditions
        self.container_statuses = container_statuses


class JobStateSchema(Schema):
    status = fields.Str()
    message = fields.Str(allow_none=True)
    details = fields.Nested(PodStateSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return JobStateConfig(**data)

    @post_dump
    def unmake(self, data):
        return JobStateConfig.remove_reduced_attrs(data)


class JobStateConfig(BaseConfig):
    SCHEMA = JobStateSchema
    IDENTIFIER = 'JobState'

    def __init__(self, status, message=None, details=None):
        self.status = status
        self.message = message
        self.details = details


class ContainerGPUResourcesSchema(Schema):
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

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ContainerGPUResourcesConfig(**data)

    @post_dump
    def unmake(self, data):
        return ContainerGPUResourcesConfig.remove_reduced_attrs(data)


class ContainerGPUResourcesConfig(BaseConfig):
    SCHEMA = ContainerGPUResourcesSchema
    IDENTIFIER = 'ContainerGPUResources'

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


class ContainerResourcesSchema(Schema):
    job_uuid = UUID()
    experiment_uuid = UUID()
    container_id = fields.Str()
    cpu_percentage = fields.Float()
    percpu_percentage = fields.List(fields.Float(), allow_none=True)
    memory_used = fields.Int()
    memory_limit = fields.Int()
    gpu_resources = fields.Nested(ContainerGPUResourcesSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ContainerResourcesConfig(**data)

    @post_dump
    def unmake(self, data):
        return ContainerResourcesConfig.remove_reduced_attrs(data)


class ContainerResourcesConfig(BaseConfig):
    SCHEMA = ContainerResourcesSchema
    IDENTIFIER = 'ContainerResources'

    def __init__(self,
                 job_uuid,
                 experiment_uuid,
                 container_id,
                 cpu_percentage,
                 percpu_percentage,
                 memory_used,
                 memory_limit,
                 gpu_resources=None):
        self.job_uuid = job_uuid
        self.experiment_uuid = experiment_uuid
        self.container_id = container_id
        self.cpu_percentage = cpu_percentage
        self.percpu_percentage = percpu_percentage
        self.memory_used = memory_used
        self.memory_limit = memory_limit
        self.gpu_resources = gpu_resources
