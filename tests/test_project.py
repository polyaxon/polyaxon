# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.project import ProjectConfig, PolyaxonSpecConfig


class TestProjectConfigs(TestCase):
    def test_validate_project_name_config(self):
        config_dict = {'name': 'test sdf', 'description': '', 'is_public': True}
        with self.assertRaises(ValidationError):
            ProjectConfig.from_dict(config_dict)

    def test_project_config(self):
        config_dict = {'name': 'test', 'description': '', 'is_public': True}
        config = ProjectConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_spec_config(self):
        config_dict = {'content': 'some content',
                       'uuid': uuid.uuid4().hex,
                       'project': uuid.uuid4().hex}
        config = PolyaxonSpecConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
