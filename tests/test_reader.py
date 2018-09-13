# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from rhea import reader


class TestReader(TestCase):
    def test_reads_yaml_files(self):
        config = reader.read('tests/fixtures/yaml_file.yml')
        assert config == {'x': 10, 'y': 20, 'foo': 'bar', 'type': 'yaml'}

    def test_reads_json_files(self):
        config = reader.read('tests/fixtures/json_file.json')
        assert config == {'x': 1, 'y': 2, 'foo': 'bar', 'type': 'json'}

    def test_reads_config_map(self):
        config = reader.read([{'x': 'y'}, {1: 2}, {'x': 'override y'}])
        assert config == {'x': 'override y', 1: 2}

        config = reader.read([{'x': 'y'},
                              {1: 2},
                              {'x': 'override y'},
                              'tests/fixtures/yaml_file.yml',
                              'tests/fixtures/json_file.json'])
        assert config == {'x': 1, 'y': 2, 1: 2, 'foo': 'bar', 'type': 'json'}

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
