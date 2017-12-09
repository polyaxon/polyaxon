# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_schemas.exceptions import PolyaxonfileError, PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification import GroupSpecification
from polyaxon_schemas.utils import to_list


class PolyaxonFile(GroupSpecification):
    """Parses Polyaxonfiles, and validate that it respects the current file specification"""

    def __init__(self, filepaths):
        filepaths = to_list(filepaths)
        for filepath in filepaths:
            if not os.path.isfile(filepath):
                raise PolyaxonfileError("`{}` must be a valid file".format(filepath))
        self._filenames = [os.path.basename(filepath) for filepath in filepaths]
        try:
            super(PolyaxonFile, self).__init__(filepaths)
        except PolyaxonConfigurationError as e:
            raise PolyaxonfileError(e)

    @property
    def filenames(self):
        return self._filenames

    @property
    def filepaths(self):
        return self.values

