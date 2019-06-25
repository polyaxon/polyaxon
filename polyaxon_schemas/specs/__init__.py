# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.build import BuildSpecification
from polyaxon_schemas.specs.experiment import ExperimentSpecification
from polyaxon_schemas.specs.group import GroupSpecification
from polyaxon_schemas.specs.job import JobSpecification
from polyaxon_schemas.specs.notebook import NotebookSpecification
from polyaxon_schemas.specs.pipelines import PipelineSpecification
from polyaxon_schemas.specs.tensorboard import TensorboardSpecification

SPECIFICATION_BY_KIND = {
    kinds.BUILD: BuildSpecification,
    kinds.EXPERIMENT: ExperimentSpecification,
    kinds.GROUP: GroupSpecification,
    kinds.JOB: JobSpecification,
    kinds.NOTEBOOK: NotebookSpecification,
    kinds.TENSORBOARD: TensorboardSpecification,
    kinds.PIPELINE: PipelineSpecification,
}
