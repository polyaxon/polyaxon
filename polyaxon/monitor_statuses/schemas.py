from marshmallow import fields

from schemas import BaseConfig, BaseSchema, JobLabelSchema


class PodStateSchema(BaseSchema):
    event_type = fields.Str()
    labels = fields.Nested(JobLabelSchema)
    phase = fields.Str()
    node_name = fields.Str(allow_none=True)
    deletion_timestamp = fields.LocalDateTime(allow_none=True)
    pod_conditions = fields.Dict(allow_none=True)
    container_statuses = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return PodStateConfig


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


class JobStateSchema(BaseSchema):
    status = fields.Str()
    created_at = fields.LocalDateTime(allow_none=True)
    message = fields.Str(allow_none=True)
    details = fields.Nested(PodStateSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return JobStateConfig


class JobStateConfig(BaseConfig):
    SCHEMA = JobStateSchema
    IDENTIFIER = 'JobState'

    def __init__(self, status, created_at=None, message=None, details=None):
        self.status = status
        self.created_at = self.localize_date(created_at)
        self.message = message
        self.details = details
