# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.run_exec import RunConfig


class TestRunConfigs(TestCase):
    def test_exec_config(self):
        config_dict = {
            'cmd': 'python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
