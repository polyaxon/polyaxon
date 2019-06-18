# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from rhea import RheaError, reader
from rhea.config import ConfigSpec


class TestReader(TestCase):
    def test_reads_yaml_files(self):
        config = reader.read('tests/fixtures/yaml_file.yml')
        assert config == {'x': 10, 'y': 20, 'foo': 'bar', 'type': 'yaml'}

    def test_reads_json_files(self):
        config = reader.read('tests/fixtures/json_file.json')
        assert config == {'x': 1, 'y': 2, 'foo': 'bar', 'type': 'json'}

    def test_reads_yaml_files_without_extension(self):
        config = reader.read(ConfigSpec('tests/fixtures/yaml_file', config_type='.yml'))
        assert config == {'x': 10, 'y': 20, 'foo': 'bar', 'type': 'yaml'}

    def test_reads_json_files_without_extension(self):
        config = reader.read(ConfigSpec('tests/fixtures/json_file', config_type='.json'))
        assert config == {'x': 1, 'y': 2, 'foo': 'bar', 'type': 'json'}

    def test_reads_non_existing_file(self):
        # Raises by default
        with self.assertRaises(RheaError):
            reader.read('tests/fixtures/no_file.yml')

        with self.assertRaises(RheaError):
            reader.read('tests/fixtures/no_file.json')

        with self.assertRaises(RheaError):
            reader.read(ConfigSpec('tests/fixtures/no_file'))

        with self.assertRaises(RheaError):
            reader.read(ConfigSpec('tests/fixtures/no_file.yml'))

        with self.assertRaises(RheaError):
            reader.read(ConfigSpec('tests/fixtures/no_file.json'))

        # Does not raise if set to ignore
        assert reader.read(ConfigSpec('tests/fixtures/no_file', check_if_exists=False)) == {}

        assert reader.read(ConfigSpec('tests/fixtures/no_file.yml', check_if_exists=False)) == {}

        assert reader.read(ConfigSpec('tests/fixtures/no_file.json', check_if_exists=False)) == {}

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

    def test_reads_non_valid_yaml_stream(self):
        stream = ";sdfsd;sdff"
        with self.assertRaises(RheaError):
            reader.read(stream)

    def test_reads_json_stream(self):
        stream = """---
        {x: y, 1: 2}
        """
        config = reader.read(stream)
        assert config is not None
