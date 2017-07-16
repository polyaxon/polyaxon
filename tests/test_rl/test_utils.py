# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np

from tensorflow.python.platform import test

from polyaxon.rl.utils import get_cumulative_rewards


class TestCumulativeRewards(test.TestCase):
    def test_cumulative_rewards(self):
        assert len(get_cumulative_rewards(range(100), range(100))) == 100

        assert np.allclose(
            get_cumulative_rewards([0, 0, 1, 0, 0, 1, 0],
                                   [False] * 7,
                                   0.9),
            [1.40049, 1.5561, 1.729, 0.81, 0.9, 1.0, 0.0])

        assert np.allclose(
            get_cumulative_rewards(
                [0, 0, 1, -2, 3, -4, 0],
                [False] * 7,
                0.5),
            [0.0625, 0.125, 0.25, -1.5, 1.0, -4.0, 0.0])

        assert np.allclose(
            get_cumulative_rewards(
                [0, 0, 1, -2, 3, -4, 0] + [-4, 0] + [3, -4, 0],
                [False, False, False, False, False, False, True, False, True, False, False, True],
                0.5),
            [0.0625, 0.125, 0.25, -1.5, 1.0, -4.0, 0.0, -4.0, 0.0, 1.0, -4.0, 0.0])

        assert np.allclose(
            get_cumulative_rewards(
                [0, 0, 1, 2, 3, 4, 0],
                [True, False, True, False, True, True, True],
                0),
            [0, 0, 1, 2, 3, 4, 0])
        print("looks good!")
