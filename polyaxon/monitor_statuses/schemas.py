from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig
from schemas.job_labels import JobLabelSchema


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
