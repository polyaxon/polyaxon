# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile
from unittest import TestCase

from polyaxon_schemas.polyaxonfile.default import (
    get_default_polyaxonfile,
    DEFAULT_POLYAXON_FILE_NAME,
    DEFAULT_POLYAXON_FILE_EXTENSION
)


class TestDefaultFile(TestCase):
    def test_default_not_found(self):
        path = tempfile.mkdtemp()
        assert get_default_polyaxonfile(path=path) is None

    def test_polyaxon_found(self):
        def create_file(path, filename, ext):
            fpath = '{}/{}.{}'.format(path, filename, ext)
            open(fpath, 'w')

        for filename in DEFAULT_POLYAXON_FILE_NAME:
            for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
                path = tempfile.mkdtemp()
                create_file(path, filename, ext)
                assert get_default_polyaxonfile(path=path)
