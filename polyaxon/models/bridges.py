# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import namedtuple

import six

import tensorflow as tf

from polyaxon.layers import FullyConnected
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import get_name_scope, get_shape, get_tensor_batch_size


class BridgeSpec(namedtuple("BridgeSpec", "encoded generated results losses loss")):

    def items(self):
        return self._asdict().items()


@six.add_metaclass(abc.ABCMeta)
class BaseBridge(GraphModule):
    """An abstract base class for defining a bridge.

    A bridge defines how state is passed between encoder and decoder.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this bridge, used for creating the scope.
        state_size: `int`. The bridge state size.
    """
    def __init__(self, mode, state_size, name="Bridge"):
        super(BaseBridge, self).__init__(mode=mode, name=name, module_type=self.ModuleType.BRIDGE)
        self.state_size = state_size

    def _get_decoder_shape(self, incoming):
        batch_size = get_tensor_batch_size(incoming)
        return tf.concat(axis=0, values=[batch_size, tf.constant(value=self.state_size)])

    def encode(self, incoming, encoder_fn, *args, **kwargs):
        """Encodes the incoming tensor.

        Args:
            incoming: `Tensor`.
            encoder_fn: `function`.
            *args:
            **kwargs:
        """
        x = encoder_fn(mode=self.mode, inputs=incoming)
        if self.state_size is None:
            self.state_size = get_shape(x)[1:]
        return x

    def decode(self, incoming, decoder_fn, *args, **kwargs):
        """Decodes the incoming tensor if it's validates against the state size of the decoder.
        Otherwise, generates a random value.

        Args:
            incoming: `Tensor`
            decoder_fn: `function`.
            *args:
            **kwargs:
        """
        incoming_shape = get_shape(incoming)
        if incoming_shape[1:] == self.state_size:
            return decoder_fn(mode=self.mode, inputs=incoming)
        else:
            if incoming_shape[0] is not None:
                shape = incoming_shape
            else:
                shape = self._get_decoder_shape(incoming)
            return decoder_fn(mode=self.mode, inputs=tf.random_normal(shape=shape))

    def _build(self, incoming, encoder_fn, decoder_fn, *args, **kwargs):
        """Subclasses should implement their logic here."""
        raise NotImplementedError


class NoOpBridge(BaseBridge):
    """A bridge that passes the encoder to the decoder outputs.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this bridge, used for creating the scope.
        state_size: `int`. The bridge state size. Default None, it will be inferred
        directly from the incoming tensor.
    """
    def __init__(self, mode, state_size=None, name="NoOpBridge"):
        super(NoOpBridge, self).__init__(mode=mode, state_size=state_size, name=name)

    def _build(self, incoming, encoder_fn, decoder_fn, *args, **kwargs):
        x = self.encode(incoming=incoming, encoder_fn=encoder_fn)
        results = self.decode(incoming=x, decoder_fn=decoder_fn)
        return BridgeSpec(encoded=x,
                          generated=self.decode(incoming=incoming, decoder_fn=decoder_fn),
                          results=results,
                          losses=None,
                          loss=None)


class LatentBridge(BaseBridge):
    """A bridge that create a latent space based on the encoder output.

    A bridge defines how latent state between the encoder and decoder.
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


BRIDGES = {
    'NoOpBridge': NoOpBridge,
    'LatentBridge': LatentBridge
}
