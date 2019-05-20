# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.api.experiment import ExperimentSchema
from polyaxon_schemas.api.group import GroupSchema
from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.fields import UUID


class ProjectSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX))
    user = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    owner = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    unique_name = fields.Str(allow_none=True)
    uuid = UUID(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    has_code = fields.Bool(allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    num_experiments = fields.Int(allow_none=True)
    num_independent_experiments = fields.Int(allow_none=True)
    num_experiment_groups = fields.Int(allow_none=True)
    num_jobs = fields.Int(allow_none=True)
    num_builds = fields.Int(allow_none=True)
    has_tensorboard = fields.Bool(allow_none=True)
    has_notebook = fields.Bool(allow_none=True)
    experiment_groups = fields.Nested(GroupSchema, many=True, allow_none=True)
    experiments = fields.Nested(ExperimentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ProjectConfig


class ProjectConfig(BaseConfig):
    SCHEMA = ProjectSchema
    IDENTIFIER = 'project'
    DEFAULT_EXCLUDE_ATTRIBUTES = [
        'id', 'uuid', 'description', 'updated_at',
        'experiment_groups', 'experiments', 'has_code', 'owner', 'user'
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at']

    def __init__(self,
                 name,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 owner=None,
                 unique_name=None,
                 uuid=None,
                 description=None,
                 is_public=True,
                 tags=None,
                 has_code=False,
                 has_tensorboard=False,
                 has_notebook=False,
                 created_at=None,
                 updated_at=None,
                 num_experiments=0,
                 num_experiment_groups=0,
                 num_independent_experiments=0,
                 num_jobs=0,
                 num_builds=0,
                 experiments=None,
                 experiment_groups=None):
        self.name = name
        self.id = id
        self.user = user
        self.owner = owner
        self.unique_name = unique_name
        self.uuid = uuid
        self.description = description
        self.is_public = is_public
        self.tags = tags
        self.has_code = has_code
        self.has_tensorboard = has_tensorboard
        self.has_notebook = has_notebook
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.num_experiments = num_experiments
        self.num_independent_experiments = num_independent_experiments
        self.num_experiment_groups = num_experiment_groups
        self.num_jobs = num_jobs
        self.num_builds = num_builds
        self.experiments = experiments
        self.experiment_groups = experiment_groups
