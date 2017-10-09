# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from polyaxon_schemas.experiment import ExperimentConfig


class TestProjectConfigs(TestCase):
    def test_project_config(self):
        config_dict = {'name': 'test', 'uuid': str(uuid.uuid4()), 'project': str(uuid.uuid4())}
        config = ExperimentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
