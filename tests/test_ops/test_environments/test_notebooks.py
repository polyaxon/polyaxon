# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig
from polyaxon_schemas.ops.notebook import NotebookConfig


class TestNotebookEnvironmentsConfigs(TestCase):

    def test_notebook_environment_config(self):
        config_dict = {
            'environment': {
                'resources': PodResourcesConfig(cpu=K8SResourcesConfig(0.5, 1)).to_dict(),
            }
        }
        config = NotebookConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict['backend'] = 'notebook'
        config = NotebookConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict['backend'] = 'lab'
        config = NotebookConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict['backend'] = 'foo'
        with self.assertRaises(ValidationError):
            NotebookConfig.from_dict(config_dict)
