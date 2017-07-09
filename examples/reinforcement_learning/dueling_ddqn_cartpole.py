# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx
import tensorflow as tf


def main(*args):
    """Creates an dqn agent for the openai gym CartPole environment."""

    env = plx.envs.GymEnvironment('CartPole-v0')

    def graph_fn(mode, inputs):
        return plx.layers.FullyConnected(mode, num_units=512)(inputs['state'])

    def model_fn(features, labels, mode):
        model = plx.models.DDQNModel(
            mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(module='huber_loss'),
            num_states=env.num_states, num_actions=env.num_actions,
            optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.01),
            exploration_config=plx.configs.ExplorationConfig(module='decay'),
            target_update_frequency=10, summaries='all')
        return model(features, labels)

    memory = plx.rl.memories.Memory(
        num_states=env.num_states, num_actions=env.num_actions, continuous=env.is_continuous)
    estimator = plx.estimators.Agent(
        model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/ddqn_cartpole")

    estimator.train(env)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
