# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx
import tensorflow as tf

from polyaxon_schemas.losses import HuberLossConfig
from polyaxon_schemas.optimizers import SGDConfig
from polyaxon_schemas.rl.explorations import DecayExplorationConfig


def main(*args):
    """Creates a normalized advantage functions agent for the openai gym Pendulum environment."""

    env = plx.envs.GymEnvironment('Pendulum-v0')

    def graph_fn(mode, features):
        return plx.layers.Dense(units=512)(features['state'])

    def model_fn(features, labels, mode):
        model = plx.models.NAFModel(
            mode, graph_fn=graph_fn,
            loss=HuberLossConfig(),
            num_states=env.num_states,
            num_actions=env.num_actions,
            optimizer=SGDConfig(learning_rate=0.01),
            exploration_config=DecayExplorationConfig(is_continuous=True),
            target_update_frequency=10,
            summaries='all')
        return model(features, labels)

    memory = plx.rl.memories.Memory()
    estimator = plx.estimators.Agent(
        model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/naf_pendulum")

    estimator.train(env)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
