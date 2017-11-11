# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.polyaxonfile import reader


class TestREader(TestCase):
    def test_reads_yaml_files(self):
        config = reader.read('tests/fixtures/simple_file.yml')
        assert config is not None

    def test_reads_json_files(self):
        config = reader.read('tests/fixtures/simple_json_file.json')
        assert config == {'x': 'y'}

    def test_reads_confi_map(self):
        config = reader.read([{'x': 'y'}, {1: 2}, {'x': 'override y'}])
        assert config == {'x': 'override y', 1: 2}

    def test_reads_yaml_stream(self):
        stream = """---
        x: y
        1: 2
        """
        config = reader.read(stream)
        assert config == {'x': 'y', 1: 2}

    def test_reads_json_stream(self):
        stream = """---
        {x: y, 1: 2}
        """
        config = reader.read(stream)
        assert config is not None
