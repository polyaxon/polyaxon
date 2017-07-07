# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from collections import namedtuple

import numpy as np

try:
    import gym
    from gym.wrappers import Monitor
    from gym.spaces import Box
    from gym.spaces.discrete import Discrete
except ImportError:
    pass


class EnvSpec(namedtuple("EnvSpec", "action state reward done next_state")):
    def items(self):
        return self._asdict().items()


class Environment(object):
    """Environment base class."""
    def __init__(self, env_id):
        self._env_id = env_id
        self._env = None
        self._closed = False

    def __str__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def reset(self, return_spec=True):
        raise NotImplementedError

    def step(self, action, state, return_spec=True):
        raise NotImplementedError

    @property
    def num_states(self):
        raise NotImplementedError

    @property
    def num_actions(self):
        raise NotImplementedError

    @property
    def is_continuous(self):
        raise NotImplementedError


class GymEnvironment(Environment):
    def __init__(self, env_id, directory=None, force=True, monitor_video=0):
        super(GymEnvironment, self).__init__(env_id=env_id)
        self._env = gym.make(env_id)

        if directory:
            if monitor_video == 0:
                video_callable = False
            else:
                video_callable = (lambda x: x % monitor_video == 0)
            self._env = Monitor(self._env, directory, video_callable=video_callable, force=force)

    def __str__(self):
        return 'OpenAIGym({})'.format(self._env_id)

    def close(self):
        if not self._closed:
            self._env.close()
            self._closed = True

    def reset(self, return_spec=True):
        state = self._env.reset()
        if return_spec:
            return EnvSpec(action=None, state=None, reward=0, done=False, next_state=state)
        return state

    def step(self, action, state, return_spec=True):
        if isinstance(action, (list, np.ndarray)):
            if isinstance(self._env.action_space, Discrete) or isinstance(action, (list, np.ndarray)):
                action = action[0]
        if isinstance(self._env.action_space, Box) and not isinstance(action, (list, np.ndarray)):
            action = list(action)
        next_state, reward, done, _ = self._env.step(action)
        if return_spec:
            return EnvSpec(
                action=action, state=state, reward=reward, done=done, next_state=next_state)
        return next_state, reward, done

    @property
    def num_states(self):
        return self._env.observation_space.shape[0]

    @property
    def num_actions(self):
        if isinstance(self._env.action_space, Box):
            return self._env.action_space.shape[0]
        else:
            return self._env.action_space.n

    @property
    def is_continuous(self):
        return not isinstance(self._env.action_space, Discrete)


ENVIRONMENTS = OrderedDict([
    ('GymEnvironment', GymEnvironment),
])
