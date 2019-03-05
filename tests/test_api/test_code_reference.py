# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.api.code_reference import CodeReferenceConfig


class TestCodeReferenceConfigs(TestCase):
    def test_code_reference_config(self):
        config_dict = {
            'id': 1,
            'commit': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'head': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'branch': 'feature1',
            'git_url': 'https://bitbucket.org:foo/bar.git',
            'is_dirty': True
        }
        config = CodeReferenceConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict = {
            'commit': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'head': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'branch': 'feature1',
            'git_url': 'https://bitbucket.org:foo/bar.git',
            'is_dirty': True
        }
        config = CodeReferenceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
