from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from scheduler.spawners.templates.base_pods import get_pod_command_args


@pytest.mark.spawner_mark
class TestPodCmdArgs(TestCase):
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

    def test_get_pod_command_args_use_args(self):
        assert get_pod_command_args(self.cmd1) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1"])
        assert get_pod_command_args(self.cmd2) == (["/bin/bash", "-c"], ["/bin/bash run.sh"])
        assert get_pod_command_args(self.cmd3) == (
            ["/bin/bash", "-c"],
            ["python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])

        assert get_pod_command_args(self.cmd4) == (
            ["/bin/bash", "-c"],
            ["video_prediction_train --model=DNA --num_masks=1 && "
             "python3 model.py "
             "--batch_size={{ batch_size }} "
             "--num_steps={{ num_steps }} "
             "--learning_rate={{ learning_rate }} "
             "--dropout={{ dropout }} "
             "--num_epochs={{ num_epochs }} "
             "--activation={{ activation }}"])
