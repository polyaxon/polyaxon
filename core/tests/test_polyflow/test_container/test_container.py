#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from mock import MagicMock

from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.containers import get_container_command_args
from tests.utils import BaseTestCase


@pytest.mark.container_mark
class TestContainerCmdArgs(BaseTestCase):
    def setUp(self):
        super().setUp()
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

        self.null_cmd1 = MagicMock()
        self.null_cmd1.command = None
        self.null_cmd1.args = None

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

    def test_none_cmd_args(self):
        assert get_container_command_args(self.null_cmd1) == ([], [])


@pytest.mark.container_mark
class TestV1ContainerCommandArgs(BaseTestCase):
    def test_exec_config_with_str_args(self):
        config_dict = {
            "name": "foo",
            "image": "test/test",
            "args": "python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (
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
            "name": "foo",
            "image": "test/test",
            "args": "foo && python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (
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
            "name": "foo",
            "image": "test/test",
            "args": "foo; python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (
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
            "name": "foo",
            "image": "test/test",
            "args": "foo || python t2t-trainer "
            "--generate_data "
            "--data_dir=~/t2t_data "
            "--problems=translate_ende_wmt32k "
            "--model=transformer "
            "--hparams_set=transformer_base_single_gpu "
            "--output_dir=~/t2t_train/base",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (
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
        config_dict = {
            "name": "foo",
            "image": "test/test",
            "command": "python t2t-trainer",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["python t2t-trainer"], [])

        config_dict = {
            "name": "foo",
            "image": "test/test",
            "command": ["python t2t-trainer"],
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["python t2t-trainer"], [])

    def test_exec_config_with_list_cmd(self):
        config_dict = {
            "name": "foo",
            "image": "test/test",
            "command": ["foo", "python t2t-trainer"],
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo", "python t2t-trainer"], [])


@pytest.mark.container_mark
class TestV1Container(BaseTestCase):
    def test_config_with_image(self):
        config_dict = {"name": "foo", "image": "foo/bar:latest"}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == ([], [])

    def test_config_str_command(self):
        config_dict = {"name": "foo", "image": "foo/bar:latest", "command": "foo"}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo"], [])

    def test_config_list_command(self):
        config_dict = {"name": "foo", "image": "foo/bar:latest", "command": ["foo"]}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo"], [])

        config_dict = {
            "name": "foo",
            "image": "foo/bar:latest",
            "command": ["foo", "bar"],
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo", "bar"], [])

    def test_config_str_args(self):
        config_dict = {"name": "foo", "image": "foo/bar:latest", "args": "foo"}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == ([], ["foo"])

    def test_config_list_args(self):
        config_dict = {"name": "foo", "image": "foo/bar:latest", "args": ["foo"]}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == ([], ["foo"])

        config_dict = {"name": "foo", "image": "foo/bar:latest", "args": ["foo", "bar"]}
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == ([], ["foo", "bar"])

    def test_config_str_command_args(self):
        config_dict = {
            "name": "foo",
            "image": "foo/bar:latest",
            "command": "foo",
            "args": "foo",
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo"], ["foo"])

    def test_config_list__command_args(self):
        config_dict = {
            "name": "foo",
            "image": "foo/bar:latest",
            "command": ["foo"],
            "args": ["foo"],
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo"], ["foo"])

        config_dict = {
            "name": "foo",
            "image": "foo/bar:latest",
            "command": ["foo", "bar"],
            "args": ["foo", "bar"],
        }
        config = k8s_schemas.V1Container(**config_dict)
        assert get_container_command_args(config) == (["foo", "bar"], ["foo", "bar"])
