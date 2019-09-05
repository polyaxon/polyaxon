# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError
from mock import MagicMock

from polyaxon_schemas.ops.container import ContainerConfig, get_container_command_args


@pytest.mark.container_mark
class TestContainerCmdArgs(TestCase):
    def setUp(self):
        self.cmd1 = MagicMock()
        self.cmd1.command = "/bin/bash"
        self.cmd1.args = "video_prediction_train --model=DNA --num_masks=1"
        self.cmd2 = MagicMock()
        self.cmd2.command = ["/bin/bash", "run.sh"]
        self.cmd2.args = None
        self.cmd3 = MagicMock()
        self.cmd3.command = ["/bin/bash", "-c"]
        self.cmd3.args = """
                python3 model.py --batch_size={{ batch_size }} \
                                 --num_steps={{ num_steps }} \
                                 --learning_rate={{ learning_rate }} \
                                 --dropout={{ dropout }} \
                                 --num_epochs={{ num_epochs }} \
                                 --activation={{ activation }}
                """
        self.cmd4 = MagicMock()
        self.cmd4.command = ["/bin/bash", "-c"]
        self.cmd4.args = """
                video_prediction_train --model=DNA --num_masks=1 && \
                python3 model.py --batch_size={{ batch_size }} \
                                 --num_steps={{ num_steps }} \
                                 --learning_rate={{ learning_rate }} \
                                 --dropout={{ dropout }} \
                                 --num_epochs={{ num_epochs }} \
                                 --activation={{ activation }}
                """
        self.cmd5 = MagicMock()
        self.cmd5.command = ["/bin/bash", "-c"]
        self.cmd5.args = """
                        video_prediction_train --model=DNA --num_masks=1 ; \
                        python3 model.py --batch_size={{ batch_size }} \
                                         --num_steps={{ num_steps }} \
                                         --learning_rate={{ learning_rate }} \
                                         --dropout={{ dropout }} \
                                         --num_epochs={{ num_epochs }} \
                                         --activation={{ activation }}
                        """
        self.cmd6 = MagicMock()
        self.cmd6.command = ["/bin/bash", "-c"]
        self.cmd6.args = """
                                video_prediction_train --model=DNA --num_masks=1 || \
                                python3 model.py --batch_size={{ batch_size }} \
                                                 --num_steps={{ num_steps }} \
                                                 --learning_rate={{ learning_rate }} \
                                                 --dropout={{ dropout }} \
                                                 --num_epochs={{ num_epochs }} \
                                                 --activation={{ activation }}
                                """

        self.list_cmd1 = MagicMock()
        self.list_cmd1.command = ["/bin/bash", "-c"]
        self.list_cmd1.args = [
            "video_prediction_train --model=DNA --num_masks=1",
            "video_prediction_train --model=NEW --num_masks=10",
        ]
        self.list_cmd2 = MagicMock()
        self.list_cmd2.command = ["/bin/bash", "-c"]
        self.list_cmd2.args = [
            "/bin/bash run1.sh",
            "/bin/bash run2.sh",
            "/bin/bash run3.sh",
        ]
        self.list_cmd3 = MagicMock()
        self.list_cmd3.command = ["/bin/bash", "-c"]
        self.list_cmd3.args = [
            "run1.sh",
            """
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """,
        ]
        self.list_cmd4 = MagicMock()
        self.list_cmd4.command = "/bin/bash"
        self.list_cmd4.args = [
            "run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 && \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """,
        ]
        self.list_cmd5 = MagicMock()
        self.list_cmd5.command = None
        self.list_cmd5.args = [
            "/bin/bash run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 ; \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """,
        ]
        self.list_cmd6 = MagicMock()
        self.list_cmd6.command = None
        self.list_cmd6.args = [
            "/bin/bash run1.sh",
            """
            video_prediction_train --model=DNA --num_masks=1 || \
            python3 model.py --batch_size={{ batch_size }} \
                             --num_steps={{ num_steps }} \
                             --learning_rate={{ learning_rate }} \
                             --dropout={{ dropout }} \
                             --num_epochs={{ num_epochs }} \
                             --activation={{ activation }}
            """,
        ]

    def test_get_container_command_args_cmd(self):
        assert get_container_command_args(self.cmd1) == (
            ["/bin/bash"],
            ["video_prediction_train --model=DNA --num_masks=1"],
        )
        assert get_container_command_args(self.cmd2) == (["/bin/bash", "run.sh"], [])
        assert get_container_command_args(self.cmd3) == (
            ["/bin/bash", "-c"],
            [
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}"
            ],
        )

        assert get_container_command_args(self.cmd4) == (
            ["/bin/bash", "-c"],
            [
                "video_prediction_train --model=DNA --num_masks=1 && "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}"
            ],
        )

        assert get_container_command_args(self.cmd5) == (
            ["/bin/bash", "-c"],
            [
                "video_prediction_train --model=DNA --num_masks=1 ; "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}"
            ],
        )

        assert get_container_command_args(self.cmd6) == (
            ["/bin/bash", "-c"],
            [
                "video_prediction_train --model=DNA --num_masks=1 || "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}"
            ],
        )

    def test_get_container_command_args_list_cmd(self):
        assert get_container_command_args(self.list_cmd1) == (
            ["/bin/bash", "-c"],
            [
                "video_prediction_train --model=DNA --num_masks=1",
                "video_prediction_train --model=NEW --num_masks=10",
            ],
        )
        assert get_container_command_args(self.list_cmd2) == (
            ["/bin/bash", "-c"],
            ["/bin/bash run1.sh", "/bin/bash run2.sh", "/bin/bash run3.sh"],
        )
        assert get_container_command_args(self.list_cmd3) == (
            ["/bin/bash", "-c"],
            [
                "run1.sh",
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}",
            ],
        )

        assert get_container_command_args(self.list_cmd4) == (
            ["/bin/bash"],
            [
                "run1.sh",
                "video_prediction_train --model=DNA --num_masks=1 && "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}",
            ],
        )

        assert get_container_command_args(self.list_cmd5) == (
            [],
            [
                "/bin/bash run1.sh",
                "video_prediction_train --model=DNA --num_masks=1 ; "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}",
            ],
        )

        assert get_container_command_args(self.list_cmd6) == (
            [],
            [
                "/bin/bash run1.sh",
                "video_prediction_train --model=DNA --num_masks=1 || "
                "python3 model.py "
                "--batch_size={{ batch_size }} "
                "--num_steps={{ num_steps }} "
                "--learning_rate={{ learning_rate }} "
                "--dropout={{ dropout }} "
                "--num_epochs={{ num_epochs }} "
                "--activation={{ activation }}",
            ],
        )


@pytest.mark.container_mark
class TestContainerConfigCommandArgs(TestCase):
    def test_exec_config_with_str_args(self):
        config_dict = {
            "image": "test/test",
            "args": "python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (
            [],
            [
                "python t2t-trainer "
                "--generate_data "
                "--data_dir=~/t2t_data "
                "--problems=translate_ende_wmt32k "
                "--model=transformer "
                "--hparams_set=transformer_base_single_gpu "
                "--output_dir=~/t2t_train/base"
            ],
        )

        config_dict = {
            "image": "test/test",
            "args": "foo && python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (
            [],
            [
                "foo && python t2t-trainer "
                "--generate_data "
                "--data_dir=~/t2t_data "
                "--problems=translate_ende_wmt32k "
                "--model=transformer "
                "--hparams_set=transformer_base_single_gpu "
                "--output_dir=~/t2t_train/base"
            ],
        )

        config_dict = {
            "image": "test/test",
            "args": "foo; python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (
            [],
            [
                "foo; python t2t-trainer "
                "--generate_data "
                "--data_dir=~/t2t_data "
                "--problems=translate_ende_wmt32k "
                "--model=transformer "
                "--hparams_set=transformer_base_single_gpu "
                "--output_dir=~/t2t_train/base"
            ],
        )

        config_dict = {
            "image": "test/test",
            "args": "foo || python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (
            [],
            [
                "foo || python t2t-trainer "
                "--generate_data "
                "--data_dir=~/t2t_data "
                "--problems=translate_ende_wmt32k "
                "--model=transformer "
                "--hparams_set=transformer_base_single_gpu "
                "--output_dir=~/t2t_train/base"
            ],
        )

    def test_exec_config_with_str_command(self):
        config_dict = {"image": "test/test", "command": "python t2t-trainer"}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (["python t2t-trainer"], [])

        config_dict = {"image": "test/test", "command": ["python t2t-trainer"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (["python t2t-trainer"], [])

    def test_exec_config_with_list_cmd(self):
        config_dict = {"image": "test/test", "command": ["foo", "python t2t-trainer"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.get_container_command_args() == (
            ["foo", "python t2t-trainer"],
            [],
        )


@pytest.mark.container_mark
class TestContainerConfig(TestCase):
    def test_config_with_image(self):
        config_dict = {"image": "foo/bar:latest"}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == ([], [])

    def test_config_with_without_image(self):
        with self.assertRaises(ValidationError):
            ContainerConfig.from_dict({})

        with self.assertRaises(ValidationError):
            ContainerConfig.from_dict({"command": ["foo"], "args": ["foo"]})

    def test_config_str_command(self):
        config_dict = {"image": "foo/bar:latest", "command": "foo"}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo"], [])

    def test_config_list_command(self):
        config_dict = {"image": "foo/bar:latest", "command": ["foo"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo"], [])

        config_dict = {"image": "foo/bar:latest", "command": ["foo", "bar"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo", "bar"], [])

    def test_config_str_args(self):
        config_dict = {"image": "foo/bar:latest", "args": "foo"}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == ([], ["foo"])

    def test_config_list_args(self):
        config_dict = {"image": "foo/bar:latest", "args": ["foo"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == ([], ["foo"])

        config_dict = {"image": "foo/bar:latest", "args": ["foo", "bar"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == ([], ["foo", "bar"])

    def test_config_str_command_args(self):
        config_dict = {"image": "foo/bar:latest", "command": "foo", "args": "foo"}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo"], ["foo"])

    def test_config_list__command_args(self):
        config_dict = {"image": "foo/bar:latest", "command": ["foo"], "args": ["foo"]}
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo"], ["foo"])

        config_dict = {
            "image": "foo/bar:latest",
            "command": ["foo", "bar"],
            "args": ["foo", "bar"],
        }
        config = ContainerConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
        assert config.get_container_command_args() == (["foo", "bar"], ["foo", "bar"])
