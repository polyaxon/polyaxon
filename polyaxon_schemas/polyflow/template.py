# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.base import BaseOneOfSchema
from polyaxon_schemas.ops.build_job import BuildConfig, BuildSchema
from polyaxon_schemas.ops.experiment import ExperimentConfig, ExperimentSchema
from polyaxon_schemas.ops.group import GroupConfig, GroupSchema
from polyaxon_schemas.ops.job import JobConfig, JobSchema
from polyaxon_schemas.ops.notebook import NotebookConfig, NotebookSchema
from polyaxon_schemas.ops.tensorboard import TensorboardConfig, TensorboardSchema


class TemplateSchema(BaseOneOfSchema):
    TYPE_FIELD = 'kind'
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        BuildConfig.IDENTIFIER: BuildSchema,
        JobConfig.IDENTIFIER: JobSchema,
        ExperimentConfig.IDENTIFIER: ExperimentSchema,
        GroupConfig.IDENTIFIER: GroupSchema,
        TensorboardConfig.IDENTIFIER: TensorboardSchema,
        NotebookConfig.IDENTIFIER: NotebookSchema,
    }
