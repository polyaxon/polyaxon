# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.ops.job import JobConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseSpecification


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

    @property
    def parallel(self):
        return self.config.parallel

    @property
    def parallel_early_stopping(self):
        early_stopping = None
        if self.parallel:
            early_stopping = self.parallel.early_stopping
        return early_stopping or []

    @property
    def parallel_algorithm(self):
        return self.parallel.algorithm.kind if self.parallel else None

    @property
    def parallel_concurrency(self):
        concurrency = None
        if self.parallel:
            concurrency = self.parallel.concurrency
        return concurrency or 1
