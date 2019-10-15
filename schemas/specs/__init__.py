# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import rhea

from schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from schemas.specs import kinds
from schemas.specs.base import BaseSpecification
from schemas.specs.job import JobSpecification
from schemas.specs.operation import OperationSpecification
from schemas.specs.pipelines import PipelineSpecification
from schemas.specs.service import ServiceSpecification

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
