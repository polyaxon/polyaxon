# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np


class Stats(object):
    """A class to collect episode rewards statistics"""
    def __init__(self):
        self.rewards = []
        self.max_reward = 0
        self.avg_reward = 0
        self.total_reward = 0

    def max(self):
        return np.max(self.rewards)

    def min(self):
        return np.min(self.rewards)

    def avg(self):
        return np.mean(self.rewards)

    def total(self):
        return np.sum(self.rewards)
