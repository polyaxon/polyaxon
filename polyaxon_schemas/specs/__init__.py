# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import rhea

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseSpecification
from polyaxon_schemas.specs.job import JobSpecification
from polyaxon_schemas.specs.operation import OperationSpecification
from polyaxon_schemas.specs.pipelines import PipelineSpecification
from polyaxon_schemas.specs.service import ServiceSpecification

SPECIFICATION_BY_KIND = {
    kinds.JOB: JobSpecification,
    kinds.SERVICE: ServiceSpecification,
    kinds.PIPELINE: PipelineSpecification,
    kinds.OPERATION: OperationSpecification,
}


def get_specification(data):
    data = rhea.read(data)
    kind = BaseSpecification.get_kind(data=data)
    try:
        return SPECIFICATION_BY_KIND[kind](data)
    except PolyaxonConfigurationError as e:
        raise PolyaxonfileError(e)
