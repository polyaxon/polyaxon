# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.specs.build import BuildSpecification
from polyaxon_schemas.specs.experiment import ExperimentSpecification
from polyaxon_schemas.specs.group import GroupSpecification
from polyaxon_schemas.specs.job import JobSpecification
from polyaxon_schemas.specs.notebook import NotebookSpecification
from polyaxon_schemas.specs.tensorboard import TensorboardSpecification

SPECIFICATION_BY_KIND = {
    BuildSpecification._SPEC_KIND: BuildSpecification,
    ExperimentSpecification._SPEC_KIND: ExperimentSpecification,
    GroupSpecification._SPEC_KIND: GroupSpecification,
    JobSpecification._SPEC_KIND: JobSpecification,
    NotebookSpecification._SPEC_KIND: NotebookSpecification,
    TensorboardSpecification._SPEC_KIND: TensorboardSpecification,
}
