# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile import reader
from polyaxon_schemas.polyaxonfile.specification import SPECIFICATION_BY_KIND
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.utils import to_list


class PolyaxonFile(object):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepaths):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]
        data = reader.read(filepaths)
        kind = BaseSpecification.get_kind(data=data)
        try:
            self.specification = SPECIFICATION_BY_KIND[kind](data)
        except PolyaxonConfigurationError as e:
            raise PolyaxonfileError(e)

    @property
    def filenames(self):
        return self._filenames
