# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.operators import ForConfig, IfConfig


class Specification(object):
    MAX_VERSION = 1.0  # Min Polyaxonfile specification version this CLI supports
    MIN_VERSION = 1.0  # Max Polyaxonfile specification version this CLI supports

    HEADERS = (
        'version', 'declarations', 'matrix',
    )
    SECTIONS = (
        'project', 'settings',
    )
    GRAPH_SECTIONS = (
        'model', 'train', 'eval'
    )
    OPERATORS = {
        ForConfig.IDENTIFIER: ForConfig,
        IfConfig.IDENTIFIER: IfConfig,
    }

    @classmethod
    def sections(cls):
        return set(cls.HEADERS + cls.SECTIONS + cls.GRAPH_SECTIONS)
