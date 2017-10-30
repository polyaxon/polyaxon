# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.run_exec import RunExecConfig
from tests.utils import assert_equal_dict


class TestRunExecConfigs(TestCase):
    def test_exce_config(self):
        config_dict = {
            'cmd': 'python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base'
        }
        config = RunExecConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
