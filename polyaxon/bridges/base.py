# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import namedtuple

import six

import tensorflow as tf


from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import get_shape, get_tensor_batch_size


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
        """Returns the decoder expected shape based on the incoming tensor."""
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
