# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase

from polyaxon_schemas.polyaxonfile import (
    DEFAULT_POLYAXON_FILE_EXTENSION,
    DEFAULT_POLYAXON_FILE_NAME,
    PolyaxonFile
)


class TestDefaultFile(TestCase):
    def test_default_not_found(self):
        path = tempfile.mkdtemp()
        assert PolyaxonFile.check_default_path(path=path) is None

    def test_polyaxon_found(self):
        def create_file(path, filename, ext):
            fpath = '{}/{}.{}'.format(path, filename, ext)
            open(fpath, 'w')

        for filename in DEFAULT_POLYAXON_FILE_NAME:
            for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
                path = tempfile.mkdtemp()
                create_file(path, filename, ext)
                assert PolyaxonFile.check_default_path(path=path)
