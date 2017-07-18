# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
from polyaxon.libs.configs import OptimizerConfig

from polyaxon.libs.utils import get_tracked
from polyaxon.models.rl.base import BasePGModel


class VPGModel(BasePGModel):
    """Implements a vanilla policy gradient model
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
        is_continuous: `bool`. Is the model built for a continuous or discrete space.
        summaries: `str` or `list`. The verbosity of the tensorboard visualization.
            Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
        clip_gradients: `float`. Gradients  clipping by global norm.
        clip_embed_gradients: `float`. Embedding gradients clipping to a specified value.
        name: `str`, the name of this model, everything will be encapsulated inside this scope.

     Returns:
        `EstimatorSpec`
    """
    def __init__(self, mode, graph_fn, num_states, num_actions, loss_config=None,
                 optimizer_config=None, eval_metrics_config=None,
                 is_deterministic=False,  is_continuous=False, summaries='all',
                 clip_gradients=0.5, clip_embed_gradients=0.1, name="Model"):

        optimizer_config = optimizer_config or OptimizerConfig('adam', learning_rate=0.004)

        super(VPGModel, self).__init__(
            mode=mode, name=name, graph_fn=graph_fn, num_states=num_states, num_actions=num_actions,
            loss_config=loss_config, optimizer_config=optimizer_config,
            eval_metrics_config=eval_metrics_config, is_deterministic=is_deterministic,
            is_continuous=is_continuous, summaries=summaries,
            clip_gradients=clip_gradients, clip_embed_gradients=clip_embed_gradients)

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        reward, action, done, = labels['reward'], labels['action'], labels['done']
        discount_reward = labels['discount_reward']

        log_probs = self._graph_results.distribution.log_prob(action)
        losses = tf.multiply(x=log_probs, y=discount_reward)
        loss = -tf.reduce_mean(losses, axis=0, name='loss')

        self._losses = losses
        self._loss = loss

        other_losses = get_tracked(tf.GraphKeys.REGULARIZATION_LOSSES)
        if other_losses:
            loss = [loss] + other_losses
            loss = tf.add_n(loss, name="TotalLoss")
            self._total_loss = loss
        return losses, loss
