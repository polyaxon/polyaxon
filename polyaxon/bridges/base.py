# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import namedtuple

import six

import tensorflow as tf

from polyaxon.libs import getters
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import get_shape, get_tensor_batch_size, get_arguments


class BridgeSpec(namedtuple("BridgeSpec", "results losses loss")):

    def items(self):
        return self._asdict().items()


@six.add_metaclass(abc.ABCMeta)
class BaseBridge(GraphModule):
    """An abstract base class for defining a bridge.

    A bridge defines how state is passed between encoder and decoder.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
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

    def encode(self, features, labels, encoder_fn, *args, **kwargs):
        """Encodes the incoming tensor.

        Args:
            features: `Tensor`.
            labels: `dict` or `Tensor`
            encoder_fn: `function`.
            *args:
            **kwargs:
        """
        if 'labels' in get_arguments(encoder_fn):
            kwargs['labels'] = labels
        output = encoder_fn(mode=self.mode, features=features, **kwargs)

        if self.state_size is None:
            self.state_size = get_shape(output)[1:]
        return output

    def decode(self, features, labels, decoder_fn, *args, **kwargs):
        """Decodes the incoming tensor if it's validates against the state size of the decoder.
        Otherwise, generates a random value.

        Args:
            features: `Tensor`
            labels: `dict` or `Tensor`
            decoder_fn: `function`.
            *args:
            **kwargs:
        """
        # TODO: make decode capable of generating values directly,
        # TODO: basically accepting None incoming values. Should also specify a distribution.

        # shape = self._get_decoder_shape(incoming)
        # return decoder_fn(mode=self.mode, inputs=tf.random_normal(shape=shape))
        if 'labels' in get_arguments(decoder_fn):
            kwargs['labels'] = labels

        return decoder_fn(mode=self.mode, features=features, **kwargs)

    def _build_loss(self, results, features, labels, loss, **kwargs):
        return getters.get_loss(loss.IDENTIFIER, results, features, **loss.to_dict())

    def _build(self,  # pylint: disable=arguments-differ
               features, labels, loss, encoder_fn, decoder_fn, *args, **kwargs):
        """Subclasses should implement their logic here and must return a `BridgeSpec`."""
        raise NotImplementedError
