# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import random

import numpy as np

from collections import deque, OrderedDict

from polyaxon_schemas.rl import memories


class Memory(object):
    """Base Agent Memory class.

    Args:
        size: `int`. The size of the memory.
        batch_size: `int`. The batch size to return during the sampling.

    Attributes:
        _size: `int`. The size of the memory.
        _batch_size: `int`. The batch size to return during the sampling.
        _memory: `deque`. Where to store the data.
        _counter: `int`. Number of step stored up to size.
        _spec: `list`. the list of keys corresponding to the data values stored each step.
    """
    def __init__(self, size=1000, batch_size=32):
        self._size = size
        self._batch_size = batch_size
        self._memory = deque()
        self._counter = 0
        self._spec = None

    def get_by_index(self, i):
        if self._counter == 0:
            return None
        return {key: self._memory[i][e] for e, key in enumerate(self._spec)}

    def can_sample(self, counter=None):
        if counter is None:
            counter = self._counter
        return counter >= self._batch_size

    def check_step_values(self, **kwargs):
        if sorted(kwargs.keys()) != self._spec:
            raise KeyError("The current values provided are different from the previous values.")

    def step(self, **kwargs):
        if self._spec is None:
            self._spec = sorted(kwargs.keys())
        else:
            self.check_step_values(**kwargs)

        values = [kwargs[k] for k in self._spec]

        if self._counter < self._size:
            self._counter += 1
        else:
            self._memory.popleft()

        self._memory.append(values)

    def sample(self):
        if not self.can_sample():
            raise ValueError('Not enough data to sample.')

        sample = {}
        batch = random.sample(self._memory, self._batch_size)
        for i, key in enumerate(self._spec):
            # pylint: disable=unsubscriptable-object
            sample[key] = np.array([b_step[i] for b_step in batch])

        return sample

    def clear(self):
        self._memory = deque()
        self._counter = 0


class BatchMemory(Memory):
    """The batch memory buffer batch size data and clear the memory after each sample."""
    def __init__(self, batch_size=5000):
        super(BatchMemory, self).__init__(batch_size, batch_size)

    def sample(self):
        if not self.can_sample():
            raise ValueError('Not enough data to sample.')

        sample = {}
        for i, key in enumerate(self._spec):
            sample[key] = np.array([b_step[i] for b_step in self._memory])

        self.clear()
        return sample


MEMORIES = OrderedDict([
    (memories.BaseMemoryConfig.IDENTIFIER, Memory),
    (memories.BatchMemoryConfig.IDENTIFIER, BatchMemory),
])
