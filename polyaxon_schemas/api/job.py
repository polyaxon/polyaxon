# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.humanize import humanize_timedelta
from marshmallow import fields, validate

from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.fields import UUID
from polyaxon_schemas.ops.environments.resources import PodResourcesSchema


class BaseJobSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    uuid = UUID(allow_none=True)
    unique_name = fields.Str(allow_none=True)
    pod_id = fields.Str(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    user = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    project = fields.Str(allow_none=True)
    build_job = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    last_status = fields.Str(allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    started_at = fields.LocalDateTime(allow_none=True)
    finished_at = fields.LocalDateTime(allow_none=True)
    total_run = fields.Str(allow_none=True)
    is_clone = fields.Bool(allow_none=True)
    content = fields.Str(allow_none=True)
    is_managed = fields.Bool(allow_none=True)
    ttl = fields.Int(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    definition = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseJobConfig


class BaseJobConfig(BaseConfig):
    SCHEMA = BaseJobSchema
    IDENTIFIER = 'Job'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'id', 'unique_name', 'user', 'last_status',
        'created_at', 'started_at', 'finished_at', 'total_run',
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at', 'started_at', 'finished_at']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 pod_id=None,
                 project=None,
                 build_job=None,
                 description=None,
                 tags=None,
                 last_status=None,
                 definition=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 content=None,
                 is_managed=None,
                 num_jobs=0,
                 resources=None,
                 ttl=None,
                 jobs=None,
                 total_run=None):
        self.id = id
        self.user = user
        self.uuid = uuid
        self.name = name
        self.unique_name = unique_name
        self.pod_id = pod_id
        self.project = project
        self.build_job = build_job
        self.description = description
        self.tags = tags
        self.last_status = last_status
        self.definition = definition
        self.started_at = self.localize_date(started_at)
        self.finished_at = self.localize_date(finished_at)
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.is_clone = is_clone
        self.content = content
        self.is_managed = is_managed
        self.num_jobs = num_jobs
        self.resources = resources
        self.ttl = ttl
        self.jobs = jobs
        self.total_run = None
        if all([self.started_at, self.finished_at]):
            self.total_run = humanize_timedelta((self.finished_at - self.started_at).seconds)


class JobSchema(BaseJobSchema):
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return JobConfig


class JobConfig(BaseJobConfig):
    SCHEMA = JobSchema
    IDENTIFIER = 'Job'
    DEFAULT_INCLUDE_ATTRIBUTES = BaseJobConfig.DEFAULT_INCLUDE_ATTRIBUTES + ['backend']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 pod_id=None,
                 project=None,
                 build_job=None,
                 description=None,
                 tags=None,
                 last_status=None,
                 definition=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 content=None,
                 is_managed=None,
                 num_jobs=0,
                 resources=None,
                 ttl=None,
                 jobs=None,
                 dockerfile=None,
                 backend=None,
                 total_run=None):
        super(JobConfig, self).__init__(
            id=id,
            user=user,
            uuid=uuid,
            name=name,
            unique_name=unique_name,
            pod_id=pod_id,
            project=project,
            build_job=build_job,
            description=description,
            tags=tags,
            last_status=last_status,
            definition=definition,
            created_at=created_at,
            updated_at=updated_at,
            started_at=started_at,
            finished_at=finished_at,
            is_clone=is_clone,
            content=content,
            is_managed=is_managed,
            num_jobs=num_jobs,
            resources=resources,
            jobs=jobs,
            ttl=ttl,
            total_run=total_run,
        )
        self.dockerfile = dockerfile
        self.backend = backend


class BuildJobSchema(BaseJobSchema):
    dockerfile = fields.Str(allow_none=True)
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return BuildJobConfig


class BuildJobConfig(BaseJobConfig):
    SCHEMA = BuildJobSchema
    IDENTIFIER = 'BuildJob'
    DEFAULT_INCLUDE_ATTRIBUTES = BaseJobConfig.DEFAULT_INCLUDE_ATTRIBUTES + ['backend']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 pod_id=None,
                 project=None,
                 build_job=None,
                 description=None,
                 tags=None,
                 last_status=None,
                 definition=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 content=None,
                 is_managed=None,
                 num_jobs=0,
                 resources=None,
                 ttl=None,
                 jobs=None,
                 dockerfile=None,
                 backend=None,
                 total_run=None):
        super(BuildJobConfig, self).__init__(
            id=id,
            user=user,
            uuid=uuid,
            name=name,
            unique_name=unique_name,
            pod_id=pod_id,
            project=project,
            build_job=build_job,
            description=description,
            tags=tags,
            last_status=last_status,
            definition=definition,
            created_at=created_at,
            updated_at=updated_at,
            started_at=started_at,
            finished_at=finished_at,
            is_clone=is_clone,
            content=content,
            is_managed=is_managed,
            num_jobs=num_jobs,
            resources=resources,
            jobs=jobs,
            ttl=ttl,
            total_run=total_run,
        )
        self.dockerfile = dockerfile
        self.backend = backend


class TensorboardJobSchema(BaseJobSchema):
    experiment = fields.Int(allow_none=True)
    experiment_group = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return TensorboardJobConfig


class TensorboardJobConfig(BaseJobConfig):
    SCHEMA = TensorboardJobSchema
    IDENTIFIER = 'TensorboardJob'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'id', 'unique_name', 'user', 'last_status', 'experiment', 'experiment_group',
        'created_at', 'started_at', 'finished_at', 'total_run', 'pod_id'
    ]

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 uuid=None,
                 name=None,
                 unique_name=None,
                 pod_id=None,
                 project=None,
                 experiment=None,
                 experiment_group=None,
                 build_job=None,
                 description=None,
                 tags=None,
                 last_status=None,
                 definition=None,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 is_clone=None,
                 content=None,
                 is_managed=None,
                 num_jobs=0,
                 resources=None,
                 ttl=None,
                 jobs=None,
                 total_run=None):
        super(TensorboardJobConfig, self).__init__(
            id=id,
            user=user,
            uuid=uuid,
            name=name,
            unique_name=unique_name,
            pod_id=pod_id,
            project=project,
            build_job=build_job,
            description=description,
            tags=tags,
            last_status=last_status,
            definition=definition,
            created_at=created_at,
            updated_at=updated_at,
            started_at=started_at,
            finished_at=finished_at,
            is_clone=is_clone,
            content=content,
            is_managed=is_managed,
            num_jobs=num_jobs,
            resources=resources,
            jobs=jobs,
            ttl=ttl,
            total_run=total_run,
        )
        self.experiment = experiment
        self.experiment_group = experiment_group


class JobStatusSchema(BaseSchema):
    id = fields.Int()
    uuid = UUID()
    job = fields.Int()
    created_at = fields.LocalDateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    traceback = fields.Str(allow_none=True)
    details = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return JobStatusConfig


class JobStatusConfig(BaseConfig):
    SCHEMA = JobStatusSchema
    IDENTIFIER = 'JobStatus'
    DATETIME_ATTRIBUTES = ['created_at']
    DEFAULT_EXCLUDE_ATTRIBUTES = ['job', 'uuid', 'details', 'traceback']

    def __init__(self,
                 id,  # pylint:disable=redefined-builtin
                 uuid,
                 job,
                 created_at,
                 status,
                 message=None,
                 traceback=None,
                 details=None):
        self.id = id
        self.uuid = uuid
        self.job = job
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.traceback = traceback
        self.details = details


class JobLabelSchema(BaseSchema):
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

    @staticmethod
    def schema_config():
        return JobLabelConfig


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
