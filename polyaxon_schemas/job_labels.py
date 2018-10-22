from marshmallow import Schema, fields, post_dump, post_load

from schemas.base import BaseConfig
from schemas.fields import UUID


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
