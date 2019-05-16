# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from mock import MagicMock

from polyaxon_schemas.ops.run import RunConfig, get_container_command_args


class TestContainerCmdArgs(TestCase):
    def setUp(self):
        self.cmd1 = MagicMock()
        self.cmd1.cmd = "video_prediction_train --model=DNA --num_masks=1"
        self.cmd2 = MagicMock()
        self.cmd2.cmd = "/bin/bash run.sh"
        self.cmd3 = MagicMock()
        self.cmd3.cmd = """
                python3 model.py --batch_size={{ batch_size }} \
                                 --num_steps={{ num_steps }} \
                                 --learning_rate={{ learning_rate }} \
                                 --dropout={{ dropout }} \
                                 --num_epochs={{ num_epochs }} \
                                 --activation={{ activation }}
                """
        self.cmd4 = MagicMock()
        self.cmd4.cmd = """
                video_prediction_train --model=DNA --num_masks=1 && \
                python3 model.py --batch_size={{ batch_size }} \
                                 --num_steps={{ num_steps }} \
                                 --learning_rate={{ learning_rate }} \
                                 --dropout={{ dropout }} \
                                 --num_epochs={{ num_epochs }} \
                                 --activation={{ activation }}
                """
        self.cmd5 = MagicMock()
        self.cmd5.cmd = """
                        video_prediction_train --model=DNA --num_masks=1 ; \
                        python3 model.py --batch_size={{ batch_size }} \
                                         --num_steps={{ num_steps }} \
                                         --learning_rate={{ learning_rate }} \
                                         --dropout={{ dropout }} \
                                         --num_epochs={{ num_epochs }} \
                                         --activation={{ activation }}
                        """
        self.cmd6 = MagicMock()
        self.cmd6.cmd = """
                                video_prediction_train --model=DNA --num_masks=1 || \
                                python3 model.py --batch_size={{ batch_size }} \
                                                 --num_steps={{ num_steps }} \
                                                 --learning_rate={{ learning_rate }} \
                                                 --dropout={{ dropout }} \
                                                 --num_epochs={{ num_epochs }} \
                                                 --activation={{ activation }}
                                """

        self.list_cmd1 = MagicMock()
        self.list_cmd1.cmd = ["video_prediction_train --model=DNA --num_masks=1",
                              "video_prediction_train --model=NEW --num_masks=10"]
        self.list_cmd2 = MagicMock()
        self.list_cmd2.cmd = ["/bin/bash run1.sh", "/bin/bash run2.sh", "/bin/bash run3.sh"]
        self.list_cmd3 = MagicMock()
        self.list_cmd3.cmd = [
            "/bin/bash run1.sh",
            """
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """]
        self.list_cmd4 = MagicMock()
        self.list_cmd4.cmd = [
            "/bin/bash run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 && \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """]
        self.list_cmd5 = MagicMock()
        self.list_cmd5.cmd = [
            "/bin/bash run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 ; \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """]
        self.list_cmd6 = MagicMock()
        self.list_cmd6.cmd = [
            "/bin/bash run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 || \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """]

    def test_get_container_command_args_cmd(self):
        assert get_container_command_args(self.cmd1) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1"])
        assert get_container_command_args(self.cmd2) == (["/bin/bash", "-c"], ["/bin/bash run.sh"])
        assert get_container_command_args(self.cmd3) == (
            ["/bin/bash", "-c"],
            ["python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.cmd4) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1 && "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.cmd5) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1 ; "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.cmd6) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1 || "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

    def test_get_container_command_args_list_cmd(self):
        assert get_container_command_args(self.list_cmd1) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1 && "
             "video_prediction_train --model=NEW --num_masks=10"])
        assert get_container_command_args(self.list_cmd2) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh && /bin/bash run2.sh && /bin/bash run3.sh"])
        assert get_container_command_args(self.list_cmd3) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh && python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.list_cmd4) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh && video_prediction_train --model=DNA --num_masks=1 && "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.list_cmd5) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh && video_prediction_train --model=DNA --num_masks=1 ; "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_container_command_args(self.list_cmd6) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh && video_prediction_train --model=DNA --num_masks=1 || "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])


class TestRunConfigs(TestCase):
    def test_exec_config_with_str_cmd(self):
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
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base']
        )

        config_dict = {
            'cmd': 'foo && python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo && python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base']
        )

        config_dict = {
            'cmd': 'foo; python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo; python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base',]
        )

        config_dict = {
            'cmd': 'foo || python t2t-trainer '
                   '--generate_data '
                   '--data_dir=~/t2t_data '
                   '--problems=translate_ende_wmt32k '
                   '--model=transformer '
                   '--hparams_set=transformer_base_single_gpu '
                   '--output_dir=~/t2t_train/base',
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_exec_config_with_list_cmd(self):
        config_dict = {
            'cmd': [
                'foo',
                'python t2t-trainer '
                '--generate_data '
                '--data_dir=~/t2t_data '
                '--problems=translate_ende_wmt32k '
                '--model=transformer '
                '--hparams_set=transformer_base_single_gpu '
                '--output_dir=~/t2t_train/base',
            ]
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo && python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base']
        )

        config_dict = {
            'cmd': [
                'foo && another_cmd && python t2t-trainer '
                '--generate_data '
                '--data_dir=~/t2t_data '
                '--problems=translate_ende_wmt32k '
                '--model=transformer '
                '--hparams_set=transformer_base_single_gpu '
                '--output_dir=~/t2t_train/base',
            ]
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo && another_cmd && python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base']
        )

        config_dict = {
            'cmd': [
                'foo && another_cmd; python t2t-trainer '
                '--generate_data '
                '--data_dir=~/t2t_data '
                '--problems=translate_ende_wmt32k '
                '--model=transformer '
                '--hparams_set=transformer_base_single_gpu '
                '--output_dir=~/t2t_train/base',
            ]
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo && another_cmd; python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base',]
        )

        config_dict = {
            'cmd': [
                'foo && another_cmd; || python t2t-trainer '
                '--generate_data '
                '--data_dir=~/t2t_data '
                '--problems=translate_ende_wmt32k '
                '--model=transformer '
                '--hparams_set=transformer_base_single_gpu '
                '--output_dir=~/t2t_train/base',
            ]
        }
        config = RunConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_cmd() == (
            ["/bin/bash", "-c"],
            ['foo && another_cmd; || python t2t-trainer '
             '--generate_data '
             '--data_dir=~/t2t_data '
             '--problems=translate_ende_wmt32k '
             '--model=transformer '
             '--hparams_set=transformer_base_single_gpu '
             '--output_dir=~/t2t_train/base']
        )
