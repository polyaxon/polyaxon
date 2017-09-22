# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx
import tensorflow as tf

from polyaxon_schemas.losses import HuberLossConfig
from polyaxon_schemas.optimizers import SGDConfig
from polyaxon_schemas.rl.explorations import DecayExplorationConfig


def main(*args):
    """Creates an double dqn agent for the openai gym CartPole environment."""

    env = plx.envs.GymEnvironment('CartPole-v0')

    def graph_fn(mode, features):
        return plx.layers.Dense(units=512)(features['state'])

    def model_fn(features, labels, mode):
        model = plx.models.DQNModel(
            mode,
            graph_fn=graph_fn,
            loss_config=HuberLossConfig(),
            num_states=env.num_states,
            num_actions=env.num_actions,
            optimizer_config=SGDConfig(learning_rate=0.01),
            exploration_config=DecayExplorationConfig(),
            target_update_frequency=10,
            dueling='mean',
            summaries='all')
        return model(features, labels)

    memory = plx.rl.memories.Memory()
    estimator = plx.estimators.Agent(
        model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/dqn_cartpole")

    estimator.train(env)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
