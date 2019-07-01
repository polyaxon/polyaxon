# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from collections import Mapping

import rhea

from hestia.list_utils import to_list

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.specs import SPECIFICATION_BY_KIND
from polyaxon_schemas.specs.base import BaseSpecification

DEFAULT_POLYAXON_FILE_NAME = [
    'polyaxon',
    'polyaxonci',
    'polyaxon-ci',
    'polyaxon.ci',
    'polyaxonfile',
]

DEFAULT_POLYAXON_FILE_EXTENSION = [
    'yaml',
    'yml',
    'json'
]


class PolyaxonFile(object):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepaths, params=None):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]
        if params:
            if not isinstance(params, Mapping):
                raise PolyaxonfileError("`{}` must be a valid mapping".format(params))
            filepaths.append({'params': params})
        data = rhea.read(filepaths)
        kind = BaseSpecification.get_kind(data=data)
        try:
            self.specification = SPECIFICATION_BY_KIND[kind](data)
        except PolyaxonConfigurationError as e:
            raise PolyaxonfileError(e)

    @property
    def filenames(self):
        return self._filenames

    @staticmethod
    def check_default_path(path):
        path = os.path.abspath(path)
        for filename in DEFAULT_POLYAXON_FILE_NAME:
            for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
                filepath = os.path.join(path, '{}.{}'.format(filename, ext))
                if os.path.isfile(filepath):
                    return filepath
