# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class ExperimentSchema(Schema):
    name = fields.Str()
    uuid = fields.UUID()
    project = fields.UUID()
    description = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentConfig(**data)


class ExperimentConfig(BaseConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'Experiment'
    REDUCED_ATTRIBUTES = ['description']

    def __init__(self, name, uuid, project, description=None):
        self.name = name
        self.uuid = uuid
        self.project = project
        self.description = description


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
    deletion_timestamp = fields.DateTime()
    pod_conditions = fields.Dict()
    container_statuses = fields.Dict()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PodStateConfig(**data)


class PodStateConfig(BaseConfig):
    SCHEMA = PodStateSchema
    IDENTIFIER = 'PodState'

    def __init__(self,
                 event_type,
                 labels,
                 phase,
                 deletion_timestamp,
                 pod_conditions,
                 container_statuses):
        self.event_type = event_type
        self.labels = labels
        self.phase = phase
        self.deletion_timestamp = deletion_timestamp
        self.pod_conditions = pod_conditions
        self.container_statuses = container_statuses


class JobStateSchema(Schema):
    status = fields.Str()
    message = fields.Str()
    details = fields.Nested(PodStateSchema)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return JobStateConfig(**data)


class JobStateConfig(BaseConfig):
    SCHEMA = JobStateSchema
    IDENTIFIER = 'JobState'

    def __init__(self, status, message, details):
        self.status = status
        self.message = message
        self.details = details
