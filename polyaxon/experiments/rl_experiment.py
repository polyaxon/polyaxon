# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import math
import os
import time

import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.python.framework import ops
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import basic_session_run_hooks, saver
from tensorflow.python.util import compat

from polyaxon import Modes
from polyaxon.estimators.agents import Agent
from polyaxon.experiments import Experiment
from polyaxon.libs import getters
from polyaxon.libs.utils import new_attr_context
from polyaxon.processing.input_data import create_input_data_fn


class RLExperiment(Experiment):
    """Experiment is a class containing all information needed to train an agent.

    After an experiment is created (by passing an Agent for training and evaluation),
    an Experiment instance knows how to invoke training and eval loops in
    a sensible fashion for distributed training.


    None of the functions passed to this constructor are executed at construction time.
    They are stored and used when a method is executed which requires it.

    Args:
        agent: Object implementing an Agent.
        train_steps: Perform this many steps of training.  default: None, means train forever.
        train_episodes: Perform this many episodes of training.  default: None, means train forever.
        first_update: First timestep to calculate `loss` and `train_op`. This is related to the
            `global_timestep` variable, number of timesteps in episodes.
        update_frequency: The frequency at which we should calculate `loss` and `train_op`.
            This frequency is related to the `gloabl_step` which is incremented every time
            we update the network.
        eval_steps: `evaluate` runs until input is exhausted (or another exception is raised),
            or for `eval_steps` steps, if specified.
        train_hooks: A list of monitors to pass to the `Agent`'s `fit` function.
        eval_hooks: A list of `SessionRunHook` hooks to pass to
            the `Agent`'s `evaluate` function.
        eval_delay_secs: Start evaluating after waiting for this many seconds.
        continuous_eval_throttle_secs: Do not re-evaluate unless the last evaluation
            was started at least this many seconds ago for continuous_eval().
        eval_every_n_steps: (applies only to train_and_evaluate).
            the minimum number of steps between evaluations. Of course, evaluation does not
            occur if no new snapshot is available, hence, this is the minimum.
        delay_workers_by_global_step: if `True` delays training workers based on global step
            instead of time.
        export_strategies: A list of `ExportStrategy`s, or a single one, or None.
        train_steps_per_iteration: (applies only to continuous_train_and_evaluate).
            Perform this many (integer) number of train steps for each training-evaluation
            iteration. With a small value, the model will be evaluated more frequently
            with more checkpoints saved. If `None`, will use a default value
            (which is smaller than `train_steps` if provided).

    Raises:
        ValueError: if `estimator` does not implement Estimator interface,
                    or if export_strategies has the wrong type.
    """

    def __init__(self, agent, env, train_steps=None, train_episodes=None,
                 first_update=5000, update_frequency=15, eval_steps=10,
                 train_hooks=None, eval_hooks=None, eval_delay_secs=0,
                 continuous_eval_throttle_secs=60, eval_every_n_steps=1,
                 delay_workers_by_global_step=False, export_strategies=None,
                 train_steps_per_iteration=100):

        if not isinstance(agent, Agent):
            raise ValueError("`estimator` must implement `Estimator`.")

        super(Experiment, self).__init__()
        self._agent = agent
        self._estimator = agent  # The estimator in this case os the agent
        self._env = env
        self._train_steps = train_steps
        self._train_episodes = train_episodes
        self._first_update = first_update
        self._update_frequency = update_frequency
        self._eval_steps = eval_steps
        self._set_export_strategies(export_strategies)
        self._train_hooks = train_hooks[:] if train_hooks else []
        self._eval_hooks = eval_hooks[:] if eval_hooks else []
        self._eval_delay_secs = eval_delay_secs
        self._continuous_eval_throttle_secs = continuous_eval_throttle_secs
        self._eval_every_n_steps = eval_every_n_steps
        self._delay_workers_by_global_step = delay_workers_by_global_step

        if train_steps_per_iteration is not None and not isinstance(train_steps_per_iteration, int):
            raise ValueError("`train_steps_per_iteration` must be an integer.")
        self._train_steps_per_iteration = train_steps_per_iteration

    @property
    def agent(self):
        return self._agent

    @property
    def train_steps(self):
        return self._train_steps

    @property
    def eval_steps(self):
        return self._eval_steps

    def _call_train(self, steps=None, first_update=None, update_frequency=None, episodes=None,
                    hooks=None, max_steps=None, max_episodes=None):
        return self._agent.train(env=self._env, first_update=first_update,
                                 update_frequency=update_frequency, episodes=episodes, steps=steps,
                                 max_steps=max_steps, max_episodes=max_episodes, hooks=hooks)

    def train(self, delay_secs=None):
        """Fit the agent.

        Train the agent for `self._train_steps` steps, after waiting for `delay_secs` seconds.
        If `self._train_steps` is `None`, train forever.

        Args:
            delay_secs: Start training after this many seconds.

        Returns:
            The trained estimator.
        """
        delay_secs, extra_hooks = self._prepare_train(delay_secs)

        return self._call_train(
            first_update=self._first_update, update_frequency=self._update_frequency,
            max_steps=self._train_steps, max_episodes=self._train_episodes,
            hooks=self._train_hooks + extra_hooks)


def create_rl_experiment(experiment_config):
    """Creates a new reinforcement learning `Experiment` instance.

    Args:
        experiment_config: the config to use for creating the experiment.
    """
    agent = getters.get_agent(experiment_config.agent_config,
                              experiment_config.model_config,
                              experiment_config.run_config)
    env = getters.get_environment(experiment_config.environment_config.module,
                                  experiment_config.environment_config.env_id,
                                  **experiment_config.environment_config.params)
    train_hooks = getters.get_hooks(experiment_config.train_hooks_config)
    eval_hooks = getters.get_hooks(experiment_config.eval_hooks_config)

    experiment = RLExperiment(
        agent=agent,
        env=env,
        train_steps=experiment_config.train_steps,
        train_episodes=experiment_config.train_episodes,
        first_update=experiment_config.first_update,
        update_frequency=experiment_config.update_frequency,
        eval_steps=experiment_config.eval_steps,
        train_hooks=train_hooks,
        eval_hooks=eval_hooks,
        eval_delay_secs=experiment_config.eval_delay_secs,
        continuous_eval_throttle_secs=experiment_config.continuous_eval_throttle_secs,
        eval_every_n_steps=experiment_config.eval_every_n_steps,
        delay_workers_by_global_step=experiment_config.delay_workers_by_global_step,
        export_strategies=experiment_config.export_strategies,
        train_steps_per_iteration=experiment_config.train_steps_per_iteration)

    return experiment
