from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import UUID


class JobLabelSchema(Schema):
    app = fields.Str(allow_none=True)
    project_name = fields.Str()
    experiment_group_name = fields.Str(allow_none=True)
    experiment_name = fields.Str(allow_none=True)
    job_name = fields.Str(allow_none=True)
    project_uuid = UUID()
    experiment_group_uuid = UUID(allow_none=True)
    experiment_uuid = UUID(allow_none=True)
    job_uuid = UUID(allow_none=True)
    task_type = fields.Str(allow_none=True)
    task_idx = fields.Str(allow_none=True)
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
    REDUCED_ATTRIBUTES = [
        'app', 'experiment_name', 'job_name', 'experiment_uuid',
        'experiment_group_name', 'experiment_group_uuid',
        'task_type', 'task_idx', 'job_uuid'
    ]

    def __init__(self,
                 project_name,
                 project_uuid,
                 role,
                 type,  # pylint:disable=redefined-builtin
                 experiment_name=None,
                 experiment_uuid=None,
                 app=None,
                 task_type=None,
                 task_idx=None,
                 job_name=None,
                 job_uuid=None,
                 experiment_group_name=None,
                 experiment_group_uuid=None,
                 **kwargs):
        self.project_name = project_name
        self.experiment_group_name = experiment_group_name
        self.experiment_name = experiment_name
        self.project_uuid = project_uuid
        self.experiment_group_uuid = experiment_group_uuid
        self.experiment_uuid = experiment_uuid
        self.task_type = task_type
        self.task_idx = task_idx
        self.job_uuid = job_uuid
        self.job_name = job_name
        self.role = role
        self.type = type
        self.app = app


class PodStateSchema(Schema):
    event_type = fields.Str()
    labels = fields.Nested(JobLabelSchema)
    phase = fields.Str()
    node_name = fields.Str(allow_none=True)
    deletion_timestamp = fields.LocalDateTime(allow_none=True)
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
    DATETIME_ATTRIBUTES = ['deletion_timestamp']

    def __init__(self,
                 event_type,
                 labels,
                 phase,
                 node_name=None,
                 deletion_timestamp=None,
                 pod_conditions=None,
                 container_statuses=None):
        self.event_type = event_type
        self.labels = labels
        self.phase = phase
        self.node_name = node_name
        self.deletion_timestamp = self.localize_date(deletion_timestamp)
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
