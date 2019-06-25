# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.ops.tensorboard import TensorboardConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseRunSpecification, BaseSpecification


class TensorboardSpecification(BaseRunSpecification):
    """The polyaxonfile specification for tensorboard.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = kinds.TENSORBOARD

    REQUIRED_SECTIONS = BaseRunSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.BUILD,
    )

    CONFIG = TensorboardConfig
