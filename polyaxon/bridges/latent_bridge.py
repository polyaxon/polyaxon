# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.bridges.base import BaseBridge, BridgeSpec
from polyaxon.layers import FullyConnected
from polyaxon.libs.utils import get_name_scope


class LatentBridge(BaseBridge):
    """A bridge that create a latent space based on the encoder output.

    A bridge defines the latent state between the encoder and decoder.
    This bridge should be used by VAE.

    Args:
        latent_dim: `int`. The latent dimension to use.
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
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

    def _build(self, incoming, encoder_fn, decoder_fn, *args, **kwargs):
        self._build_dependencies()
        encoded = self.encode(incoming=incoming, encoder_fn=encoder_fn)
        z_mean = self.z_mean(encoded)
        z_log_sigma = self.z_log_sigma(encoded)

        shape = self._get_decoder_shape(incoming)
        eps = tf.random_normal(shape=shape, mean=self.mean, stddev=self.stddev,
                               dtype=tf.float32, name='eps')
        z = tf.add(z_mean, tf.multiply(tf.sqrt(tf.exp(z_log_sigma)), eps))
        decoded = self.decode(incoming=z, decoder_fn=decoder_fn)
        with get_name_scope('latent_loss') as scope_:
            losses = -0.5 * tf.reduce_sum(
                1 + z_log_sigma - tf.square(z_mean) - tf.exp(z_log_sigma), axis=1)
            loss = tf.losses.compute_weighted_loss(losses, 1.0, scope_, tf.GraphKeys.LOSSES)
        return BridgeSpec(encoded=z_mean,
                          generated=self.decode(incoming=incoming, decoder_fn=decoder_fn),
                          results=decoded,
                          losses=losses,
                          loss=loss)

