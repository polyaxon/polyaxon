# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile


class TestPolyaxonfile(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_version.yml'))

    def test_missing_model_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_model.yml'))

    def test_missing_project_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_project.yml'))

    def test_simple_file_passes(self):
        PolyaxonFile(os.path.abspath('tests/fixtures/simple_file.yml'))

    def test_advanced_file_passes(self):
        PolyaxonFile(os.path.abspath('tests/fixtures/advanced_file.yml'))
