# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import tensorflow as tf

from polyaxon.layers.core import Dense
from polyaxon.models.rl.base import BaseQModel


class NAFModel(BaseQModel):
    """Implements a normalized advantage functions model.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        graph_fn: Graph function. Follows the signature:
            * Args:
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `inputs`: the feature inputs.
        loss: An instance of `LossConfig`.
        num_states: `int`. The number of states.
        num_actions: `int`. The number of actions.
        optimizer: An instance of `OptimizerConfig`. Default value `Adam`.
        metrics: a list of `MetricConfig` instances.
        discount: `float`. The discount factor on the target Q values.
        exploration_config: An instance `ExplorationConfig`
        use_target_graph: `bool`. To use a second “target” network,
            which we will use to compute target Q values during our updates.
        target_update_frequency: `int`. At which frequency to update the target graph.
            Only used when `use_target_graph` is set tot True.
        is_continuous: `bool`. Is the model built for a continuous or discrete space.
        use_expert_demo: Whether to pretrain the model on a human/expert data.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

     Returns:
        `EstimatorSpec`
    """

    def __init__(self,
                 mode,
                 graph_fn,
                 loss,
                 num_states,
                 num_actions,
                 optimizer=None,
                 metrics=None,
                 discount=0.97,
                 exploration_config=None,
                 use_target_graph=True,
                 target_update_frequency=5,
                 is_continuous=True,
                 use_expert_demo=False,
                 summaries='all',
                 clip_gradients=0.5,
                 clip_embed_gradients=0.1,
                 name="Model"):
        super(NAFModel, self).__init__(mode=mode,
                                       graph_fn=graph_fn,
                                       loss=loss,
                                       num_states=num_states,
                                       num_actions=num_actions,
                                       optimizer=optimizer,
                                       metrics=metrics,
                                       discount=discount,
                                       exploration_config=exploration_config,
                                       use_target_graph=use_target_graph,
                                       target_update_frequency=target_update_frequency,
                                       is_continuous=is_continuous,
                                       dueling=True,
                                       use_expert_demo=use_expert_demo,
                                       summaries=summaries,
                                       clip_gradients=clip_gradients,
                                       clip_embed_gradients=clip_embed_gradients,
                                       name=name)

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        reward, action, done = labels['reward'], labels['action'], labels['done']

        # Lower triangle matrix
        lt_size = self.num_actions * (self.num_actions + 1) // 2
        lt_entries = Dense(units=lt_size)(self._train_results.graph_outputs)
        lt_matrix = tf.exp(tf.map_fn(tf.diag, lt_entries[:, :self.num_actions]))

        if self.num_actions > 1:
            offset = self.num_actions
            l_columns = list()
            for i, size in enumerate(xrange(self.num_actions - 1, 0, -1), 1):
                column = tf.pad(lt_entries[:, offset: offset + size], ((0, 0), (i, 0)))
                l_columns.append(column)
                offset += size
            lt_matrix += tf.stack(l_columns, 1)

        # P = LL^T
        p_matrix = tf.matmul(lt_matrix, tf.transpose(lt_matrix, (0, 2, 1)))
        action_diff = action - self._train_results.a

        # A = (a - mean)P(a - mean) / 2
        advantage = -tf.matmul(tf.expand_dims(action_diff, 1),
                               tf.matmul(p_matrix, tf.expand_dims(action_diff, 2))) / 2
        advantage = tf.squeeze(advantage, 2)

        # Q = V(s) + A(s, a)
        train_q_value = (self._train_results.v + advantage)[:-1]
        target_q_value = (reward[:-1] + (1.0 - tf.cast(done[:-1], tf.float32)) *
                          self.discount * self._target_results.v[1:])

        return super(NAFModel, self)._build_loss(train_q_value, features, target_q_value)
