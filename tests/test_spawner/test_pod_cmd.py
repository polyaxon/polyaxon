from unittest import TestCase
from unittest.mock import MagicMock

from scheduler.spawners.templates.base_pods import get_pod_command_args


class TestPodCmdArgs(TestCase):
    def test_get_pod_command_args(self):
        cmd1 = MagicMock()
        cmd1.cmd = "video_prediction_train --model=DNA --num_masks=1"
        cmd2 = MagicMock()
        cmd2.cmd = "/bin/bash run.sh"
        cmd3 = MagicMock()
        cmd3.cmd = """
        python3 model.py --batch_size={{ batch_size }} \
                         --num_steps={{ num_steps }} \
                         --learning_rate={{ learning_rate }} \
                         --dropout={{ dropout }} \
                         --num_epochs={{ num_epochs }} \
                         --activation={{ activation }}
        """
        assert get_pod_command_args(cmd1) == (['video_prediction_train',
                                               '--model=DNA',
                                               '--num_masks=1'], [])
        assert get_pod_command_args(cmd2) == (['/bin/bash', 'run.sh'], [])
        assert get_pod_command_args(cmd3) == (['python3',
                                               'model.py',
                                               '--batch_size={{', 'batch_size', '}}',
                                               '--num_steps={{', 'num_steps', '}}',
                                               '--learning_rate={{', 'learning_rate', '}}',
                                               '--dropout={{', 'dropout', '}}',
                                               '--num_epochs={{', 'num_epochs', '}}',
                                               '--activation={{', 'activation', '}}'], [])
