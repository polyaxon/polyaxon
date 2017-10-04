# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.operators import ForConfig, IfConfig


class Specification(object):
    """The polyaxonfile specification.

    HEADERS:
        version: the version of the file to be parsed and validated.
        matrix: hyper parameters matrix definition.
        declarations: variables/modules that can be reused.

    SECTIONS:

    """
    MAX_VERSION = 1.0  # Min Polyaxonfile specification version this CLI supports
    MIN_VERSION = 1.0  # Max Polyaxonfile specification version this CLI supports

    VERSION = 'version'
    PROJECT = 'project'
    MATRIX = 'matrix'
    DECLARATIONS = 'declarations'
    SETTINGS = 'settings'
    ENVIRONMENT = 'environment'
    MODEL = 'model'
    TRAIN = 'train'
    EVAL = 'eval'

    SECTIONS = (
        VERSION, PROJECT, MATRIX, DECLARATIONS, SETTINGS, ENVIRONMENT, MODEL, TRAIN, EVAL
    )

    GRAPH_SECTIONS = (
        MODEL, TRAIN, EVAL
    )

    REQUIRED_SECTIONS = (
        VERSION, PROJECT, MODEL
    )

    OPERATORS = {
        ForConfig.IDENTIFIER: ForConfig,
        IfConfig.IDENTIFIER: IfConfig,
    }
