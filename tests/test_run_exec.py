# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.run_exec import RunExecConfig


class TestRunExecConfigs(TestCase):
    def test_exce_config(self):
        config_dict = {
            'cmd': 'python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
            'image': 'some_image_name',
        }
        config = RunExecConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_exce_from_git_repo_with_install_step_config(self):
        config_dict = {
            'cmd': 'python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
            'image': 'tensorflow:1.3.0',
            'build_steps': ['pip install tensor2tensor'],
            'env_vars': [['LC_ALL', 'en_US.UTF-8']],
            'git': 'https://github.com/tensorflow/tensor2tensor.git'
        }
        config = RunExecConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
