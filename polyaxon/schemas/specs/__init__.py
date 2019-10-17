# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import rhea

from polyaxon.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon.schemas.specs import kinds
from polyaxon.schemas.specs.base import BaseSpecification
from polyaxon.schemas.specs.job import JobSpecification
from polyaxon.schemas.specs.operation import OperationSpecification
from polyaxon.schemas.specs.pipelines import PipelineSpecification
from polyaxon.schemas.specs.service import ServiceSpecification

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
