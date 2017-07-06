# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import numpy as np

from polyaxon.rl.environments import EnvSpec


class BaseMemory(object):
    """Base Agent Memory class."""
    def __init__(self, num_states, num_actions, continuous, size=1000, batch_size=32):
        self.size = size
        self.batch_size = batch_size

        self.state = np.empty((self.size, num_states), dtype=np.float32)
        if continuous:
            self.action = np.empty((self.size, num_actions), dtype=np.float32)
        else:
            self.action = np.empty(self.size, dtype=np.int8)
        self.reward = np.empty(self.size)
        self.next_state = np.empty((self.size, num_states), dtype=np.float32)
        self.done = np.empty(self.size, dtype=np.bool)

        self.counter = 0

    @property
    def can_sample(self):
        return self.counter >= self.batch_size

    def step(self, env_spec):
        raise NotImplementedError

    def sample(self):
        raise NotImplementedError


class Memory(BaseMemory):
    """Simple Agent Memory class."""

    def step(self, env_spec):
        assert isinstance(env_spec, EnvSpec)
        idx = self.counter % self.size
        self.state[idx][:] = env_spec.state
        self.action[idx] = env_spec.action
        self.reward[idx] = env_spec.reward
        self.next_state[idx][:] = env_spec.next_state
        self.done[idx] = env_spec.done

        self.counter += 1

    def sample(self):
        if not self.can_sample:
            raise ValueError('Not enough data to sample.')

        max_idx = self.counter if self.counter < self.size else self.size
        sampled_idx = np.random.randint(0, max_idx, size=self.batch_size)
        return EnvSpec(
            state=self.state[sampled_idx],
            action=self.action[sampled_idx],
            reward=self.reward[sampled_idx],
            done=self.done[sampled_idx],
            next_state=self.next_state[sampled_idx],
        )


MEMORIES = OrderedDict([
    ('Memory', Memory),
])
