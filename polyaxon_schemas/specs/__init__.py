# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.job import JobSpecification
from polyaxon_schemas.specs.pipelines import PipelineSpecification
from polyaxon_schemas.specs.service import ServiceSpecification

SPECIFICATION_BY_KIND = {
    kinds.JOB: JobSpecification,
    kinds.SERVICE: ServiceSpecification,
    kinds.PIPELINE: PipelineSpecification,
}
