# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from schemas.ops.service import ServiceConfig
from schemas.specs import kinds
from schemas.specs.base import BaseSpecification


class ServiceSpecification(BaseSpecification):
    """The polyaxonfile specification for notebooks.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
    """

    _SPEC_KIND = kinds.SERVICE

    REQUIRED_SECTIONS = BaseSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.CONTAINER,
    )

    CONFIG = ServiceConfig
