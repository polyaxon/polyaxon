# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.environments import PodResourcesSchema
from polyaxon_schemas.utils import UUID, humanize_timedelta


class JobSchema(Schema):
    id = fields.Int(allow_none=True)
    uuid = UUID(allow_none=True)
    unique_name = fields.Str(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    user = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    project = UUID(allow_none=True)
    project_name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    last_status = fields.Str(allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    started_at = fields.LocalDateTime(allow_none=True)
    finished_at = fields.LocalDateTime(allow_none=True)
    total_run = fields.Str(allow_none=True)
    is_running = fields.Bool(allow_none=True)
    is_done = fields.Bool(allow_none=True)
    is_clone = fields.Bool(allow_none=True)
    config = fields.Dict(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    definition = fields.Dict(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return JobConfig(**data)

    @post_dump
    def unmake(self, data):
        return JobConfig.remove_reduced_attrs(data)


class JobConfig(BaseConfig):
    SCHEMA = JobSchema
    IDENTIFIER = 'Job'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'id', 'unique_name', 'user', 'experiment_group_name', 'last_status',
        'created_at', 'started_at', 'finished_at', 'total_run', 'is_done', 'is_running'
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at', 'started_at', 'finished_at']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 project=None,
                 project_name=None,
                 experiment_group=None,
                 experiment_group_name=None,
                 description=None,
                 tags=None,
                 last_status=None,
                 definition=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 is_running=None,
                 is_done=None,
                 config=None,
                 num_jobs=0,
                 resources=None,
                 jobs=None,
                 total_run=None):
        self.id = id
        self.user = user
        self.uuid = uuid
        self.name = name
        self.unique_name = unique_name
        self.project = project
        self.project_name = project_name
        self.experiment_group = experiment_group
        self.experiment_group_name = experiment_group_name
        self.description = description
        self.tags = tags
        self.last_status = last_status
        self.definition = definition
        self.started_at = self.localize_date(started_at)
        self.finished_at = self.localize_date(finished_at)
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.is_running = is_running
        self.is_done = is_done
        self.is_clone = is_clone
        self.config = config  # The json compiled content of this experiment
        self.num_jobs = num_jobs
        self.resources = resources
        self.jobs = jobs
        self.total_run = None
        if all([self.started_at, self.finished_at]):
            self.total_run = humanize_timedelta((self.finished_at - self.started_at).seconds)


class JobStatusSchema(Schema):
    uuid = UUID()
    job = UUID()
    created_at = fields.LocalDateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    details = fields.Dict(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return JobStatusConfig(**data)

    @post_dump
    def unmake(self, data):
        return JobStatusConfig.remove_reduced_attrs(data)


class JobStatusConfig(BaseConfig):
    SCHEMA = JobStatusSchema
    IDENTIFIER = 'ExperimentStatus'
    DATETIME_ATTRIBUTES = ['created_at']
    DEFAULT_EXCLUDE_ATTRIBUTES = ['job', 'uuid']

    def __init__(self, uuid, job, created_at, status, message=None, details=None):
        self.uuid = uuid
        self.job = job
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.details = details
