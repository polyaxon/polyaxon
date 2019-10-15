# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from schemas.ops.job import JobConfig
from schemas.specs import kinds
from schemas.specs.base import BaseSpecification


class JobSpecification(BaseSpecification):
    """The polyaxonfile specification for run jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        CONTAINER: defines the run step where the user can run a command
    """

    _SPEC_KIND = kinds.JOB

    REQUIRED_SECTIONS = BaseSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.CONTAINER,
    )

    CONFIG = JobConfig
