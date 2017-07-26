# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon import Modes
from polyaxon.bridges.base import BaseBridge, BridgeSpec
from polyaxon.layers import FullyConnected
from polyaxon.libs import getters
from polyaxon.libs.utils import get_name_scope


class LatentBridge(BaseBridge):
    """A bridge that create a latent space based on the encoder output.

    This bridge could be used by VAE.

    Args:
        latent_dim: `int`. The latent dimension to use.
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`. The name of this subgraph, used for creating the scope.

    Attributes:
        z_mean: `Tensor`. The latent distribution mean.
        z_log_sigma: `Tensor`. The latent distribution log variance.
    """
    def __init__(self, mode, latent_dim=1, state_size=None, mean=0., stddev=1.,
                 name="LatentBridge"):
        state_size = state_size or [latent_dim]
        super(LatentBridge, self).__init__(mode=mode, state_size=state_size, name=name)
        self.latent_dim = latent_dim
        self.mean = mean
        self.stddev = stddev

    def _build_dependencies(self):
        self.z_mean = FullyConnected(self.mode, num_units=self.latent_dim, name='z_mean')
        self.z_log_sigma = FullyConnected(self.mode, num_units=self.latent_dim, name='z_log_sigma')

    def _build_loss(self, results, features, labels, loss_config, **kwargs):
        losses, loss = getters.get_loss(loss_config.module, results, features, **loss_config.params)

        with get_name_scope('latent_loss'):
            z_mean = kwargs['z_mean']
            z_log_sigma = kwargs['z_log_sigma']

            latent_losses = -0.5 * tf.reduce_sum(
                1 + z_log_sigma - tf.square(z_mean) - tf.exp(z_log_sigma))
            latent_loss = tf.losses.compute_weighted_loss(latent_losses)

        losses += latent_losses
        loss += latent_loss
        return losses, loss

    def _build(self, features, labels, loss_config, encoder_fn, decoder_fn, *args, **kwargs):
        self._build_dependencies()

        losses = None
        loss = None
        if Modes.GENERATE == self.mode:
            results = self.decode(features=features, labels=labels, decoder_fn=decoder_fn)
        elif Modes.ENCODE == self.mode:
            encoded = self.encode(features=features, labels=labels, encoder_fn=encoder_fn)
            results = self.z_mean(encoded)
        else:
            encoded = self.encode(features=features, labels=labels, encoder_fn=encoder_fn)
            z_mean = self.z_mean(encoded)
            z_log_sigma = self.z_log_sigma(encoded)
            shape = self._get_decoder_shape(features)
            eps = tf.random_normal(
                shape=shape, mean=self.mean, stddev=self.stddev, dtype=tf.float32, name='eps')
            z = tf.add(z_mean, tf.multiply(tf.sqrt(tf.exp(z_log_sigma)), eps))
            results = self.decode(features=z, labels=labels, decoder_fn=decoder_fn)
            losses, loss = self._build_loss(results, features, labels, loss_config,
                                            z_mean=z_mean,
                                            z_log_sigma=z_log_sigma)

        return BridgeSpec(results=results, losses=losses, loss=loss)

