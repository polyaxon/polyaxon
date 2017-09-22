# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx
import tensorflow as tf


def main(*args):
    """Creates an double dqn agent for the openai gym CartPole environment."""

    env = plx.envs.GymEnvironment('CartPole-v0')

    def graph_fn(mode, features):
        return plx.layers.Dense(units=512)(features['state'])

    def model_fn(features, labels, mode):
        model = plx.models.VPGModel(
            mode,
            graph_fn=graph_fn,
            num_states=env.num_states,
            num_actions=env.num_actions,
            summaries='all')
        return model(features, labels)

    memory = plx.rl.memories.BatchMemory()
    estimator = plx.estimators.PGAgent(
        model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/vpg_cartpole")

    estimator.train(env)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
