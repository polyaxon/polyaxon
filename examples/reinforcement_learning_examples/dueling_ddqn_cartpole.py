# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.losses import HuberLossConfig
from polyaxon_schemas.optimizers import SGDConfig
from polyaxon_schemas.rl.explorations import DecayExplorationConfig

import polyaxon as plx
import tensorflow as tf


def main(*args):
    """Creates an dqn agent for the openai gym CartPole environment."""

    env = plx.envs.GymEnvironment('CartPole-v0')

    def graph_fn(mode, features):
        return plx.layers.Dense(units=512)(features['state'])

    def model_fn(features, labels, mode):
        model = plx.models.DDQNModel(
            mode,
            graph_fn=graph_fn,
            loss_config=HuberLossConfig(),
            num_states=env.num_states,
            num_actions=env.num_actions,
            optimizer_config=SGDConfig(learning_rate=0.01),
            exploration_config=DecayExplorationConfig(),
            target_update_frequency=10,
            summaries='all')
        return model(features, labels)

    memory = plx.rl.memories.Memory()
    estimator = plx.estimators.Agent(
        model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/ddqn_cartpole")

    estimator.train(env)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
