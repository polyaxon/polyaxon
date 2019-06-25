# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.cached_property import cached_property

from polyaxon_schemas.ops.notebook import NotebookConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseRunSpecification, BaseSpecification


class NotebookSpecification(BaseRunSpecification):
    """The polyaxonfile specification for notebooks.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = kinds.NOTEBOOK

    REQUIRED_SECTIONS = BaseRunSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.BUILD,
    )

    ENVIRONMENT_CONFIG = NotebookConfig
    CONFIG = NotebookConfig

    @cached_property
    def backend(self):
        return self.config.backend
