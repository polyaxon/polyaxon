# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from gym.wrappers import Monitor
from gym.spaces import Box
from gym.spaces.discrete import Discrete


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

    def reset(self):
        raise NotImplementedError

    def step(self, action):
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

    def reset(self):
        return self._env.reset()

    def step(self, action):
        if isinstance(self._env.action_space, Box) and not isinstance(action, list):
            action = list(action)
        state, reward, done, _ = self._env.step(action)
        return state, reward, done

    @property
    def num_states(self):
        return self._env.observation_space.shape

    @property
    def num_actions(self):
        return self._env.action_space.shape

    @property
    def is_continuous(self):
        return not isinstance(self._env.action_space, Discrete)
