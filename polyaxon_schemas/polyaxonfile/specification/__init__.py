# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile.specification.build import BuildSpecification
from polyaxon_schemas.polyaxonfile.specification.experiment import ExperimentSpecification
from polyaxon_schemas.polyaxonfile.specification.group import GroupSpecification
from polyaxon_schemas.polyaxonfile.specification.job import JobSpecification
from polyaxon_schemas.polyaxonfile.specification.plugin import (
    NotebookSpecification,
    TensorboardSpecification
)

SPECIFICATION_BY_KIND = {
    BuildSpecification._SPEC_KIND: BuildSpecification,
    ExperimentSpecification._SPEC_KIND: ExperimentSpecification,
    GroupSpecification._SPEC_KIND: GroupSpecification,
    JobSpecification._SPEC_KIND: JobSpecification,
    NotebookSpecification._SPEC_KIND: NotebookSpecification,
    TensorboardSpecification._SPEC_KIND: TensorboardSpecification,
}
