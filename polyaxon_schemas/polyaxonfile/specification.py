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
    SETTINGS = 'settings'
    MATRIX = 'matrix'
    DECLARATIONS = 'declarations'
    ENVIRONMENT = 'environment'
    RUN_EXEC = 'run'
    MODEL = 'model'
    TRAIN = 'train'
    EVAL = 'eval'

    SECTIONS = (
        VERSION, PROJECT, ENVIRONMENT, MATRIX, DECLARATIONS, SETTINGS, RUN_EXEC, MODEL, TRAIN, EVAL
    )

    HEADER_SECTIONS = (
        VERSION, PROJECT, SETTINGS
    )

    GRAPH_SECTIONS = (
        MODEL, TRAIN, EVAL
    )

    REQUIRED_SECTIONS = (
        VERSION, PROJECT
    )

    OPERATORS = {
        ForConfig.IDENTIFIER: ForConfig,
        IfConfig.IDENTIFIER: IfConfig,
    }
