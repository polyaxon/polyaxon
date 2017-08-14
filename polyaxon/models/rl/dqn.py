# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.layers import OneHotEncoding
from polyaxon.models.rl.base import BaseQModel


class DQNModel(BaseQModel):
    """Implements a double deep Q model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        loss_config: An instance of `LossConfig`.
        num_states: `int`. The number of states.
        num_actions: `int`. The number of actions.
        optimizer_config: An instance of `OptimizerConfig`. Default value `Adam`.
        eval_metrics_config: a list of `MetricConfig` instances.
        discount: `float`. The discount factor on the target Q values.
        exploration_config: An instance `ExplorationConfig`
        use_target_graph: `bool`. To use a second “target” network,
            which we will use to compute target Q values during our updates.
        update_frequency: `int`. At which frequency to update the target graph.
            Only used when `use_target_graph` is set tot True.
        is_continuous: `bool`. Is the model built for a continuous or discrete space.
        dueling: `str` or `bool`. To compute separately the advantage and value functions.
            Options:
                * `True`: creates advantage and state value without any further computation.
                * `mean`, `max`, and `naive`: creates advantage and state value, and computes
                  Q = V(s) + A(s, a)
                  where A = A - mean(A) or A = A - max(A) or A = A.
        use_expert_demo: Whether to pretrain the model on a human/expert data.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

     Returns:
        `EstimatorSpec`
    """

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        reward, action, done = labels['reward'], labels['action'], labels['done']
        target_q_values = tf.reduce_max(self._target_results.q, axis=1)

        action_selector = OneHotEncoding(mode=self.mode, n_classes=self.num_actions)(action[:-1])
        train_q_value = tf.reduce_sum(
            tf.multiply(self._train_results.q[:-1], action_selector), axis=1)

        target_q_value = (reward[:-1] + (1.0 - tf.cast(done[:-1], tf.float32)) *
                          self.discount * target_q_values[1:])
        return super(DQNModel, self)._build_loss(train_q_value, features, target_q_value)
