# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf

try:
    from tensorflow.python.ops.distributions.categorical import Categorical
    from tensorflow.python.ops.distributions.normal import Normal
    from tensorflow.python.ops.distributions.kullback_leibler import kl_divergence
except ImportError:
    # tf < 1.2.0
    from tensorflow.contrib.distributions import Categorical, Normal, kl as kl_divergence

from polyaxon.libs.utils import get_shape
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
    def get_vars_grads(self, loss, variables):
        grads = tf.gradients(loss, variables)
        grads_and_vars = list(zip(grads, variables))
        return grads_and_vars, tf.concat(
            values=[tf.reshape(grad, (-1, )) for (grad, v) in grads_and_vars], axis=0)

    def _build_loss(self, results, features, labels):
        """Creates the loss operation

        Returns:
             tuple `(losses, loss)`:
                `losses` are the per-batch losses.
                `loss` is a single scalar tensor to minimize.
        """
        reward, action, done, = labels['reward'], labels['action'], labels['done']
        discount_reward = labels['discount_reward']
        dist_values = labels['dist_values']
        tangents = labels.get('tangents')
        theta = labels.get('theta')

        old_distribution = self._build_distribution(values=dist_values)
        log_probs = self._graph_results.distribution.log_prob(action)
        old_log_probs = old_distribution.log_prob(action)

        self._losses = tf.multiply(x=tf.exp(log_probs - old_log_probs), y=discount_reward)
        self._surrogate_loss = -tf.reduce_mean(self._losses, axis=0, name='surrogate_loss')
        entropy = self._graph_results.distribution.entropy()
        self._entropy_loss = tf.reduce_mean(entropy, name='entropy_loss')
        kl_divergence_value = kl_divergence(self._graph_results.distribution, old_distribution)
        self._kl_loss = tf.reduce_mean(kl_divergence_value, name='kl_loss')

        if self.is_continuous:
            dist_values_fixed = tf.stop_gradient(
                tf.concat(values=[self._graph_results.distribution.loc,
                                  self._graph_results.distribution.scale], axis=0))
        else:
            dist_values_fixed = tf.stop_gradient(self._graph_results.distribution.logits)
        distribution_1_fixed = self._build_distribution(values=dist_values_fixed)
        kl_divergence_1_fixed = kl_divergence(
            distribution_1_fixed, self._graph_results.distribution)
        self._kl_loss_1_fixed = tf.reduce_mean(kl_divergence_1_fixed, name='kl_loss_1_fixed')

        variables = list(tf.trainable_variables())
        self._loss = self._surrogate_loss
        self._grads_and_vars, self._policy_gradient = self.get_vars_grads(
            [self._surrogate_loss], variables)

        offset = 0
        list_tangents = []
        list_assigns = []
        for variable in variables:
            shape = get_shape(variable)
            size = np.prod(shape)
            list_tangents.append(tf.reshape(tangents[offset:offset + size], shape))
            list_assigns.append(tf.assign(variable, tf.reshape(theta[offset:offset + size], shape)))
            offset += size

        gradients = tf.gradients(self._kl_loss_1_fixed, variables)
        gradient_vector_product = [tf.reduce_sum(g * t) for (g, t) in zip(gradients, list_tangents)]
        _, self._fisher_vector_product = self.get_vars_grads(gradient_vector_product, variables)

        self._set_theta = tf.group(*list_assigns)
        self._get_theta = tf.concat(axis=0,
                                    values=[tf.reshape(variable, (-1,)) for variable in variables])
        return self._losses, self._loss

    def _build_predictions(self, results, features, labels):
        """Creates the dictionary of predictions that is returned by the model."""
        predictions = super(BasePGModel, self)._build_predictions(
            results=results, features=features, labels=labels)
        predictions['graph_results'] = self._graph_results.graph_outputs
        predictions['a'] = self._graph_results.a
        predictions['dist_values'] = self._graph_results.dist_values
        predictions['policy_gradient'] = self._policy_gradient
        predictions['fisher_vector_product'] = self._fisher_vector_product
        return predictions

    def _build_extra_ops(self, results, features, labels):
        return {'set_theta': self._set_theta,
                'get_theta': self._get_theta}
