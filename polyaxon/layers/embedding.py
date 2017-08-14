# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf

from polyaxon.libs import getters
from polyaxon.libs.template_module import BaseLayer
from polyaxon.libs.utils import get_shape, track
from polyaxon.variables import variable


class Embedding(BaseLayer):
    """Embedding layer for a sequence of integer ids or floats.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        input_dim: list of `int`. Vocabulary size (number of ids).
        output_dim: list of `int`. Embedding size.
        validate_indices: `bool`. Whether or not to validate gather indices.
        weights_init: `str` (name) or `Tensor`. Weights initialization.
            Default: 'truncated_normal'.
        trainable: `bool`. If True, weights will be trainable.
        restore: `bool`. If True, this layer weights will be restored when
            loading a model.
        name: A name for this layer (optional). Default: 'Embedding'.
    """
    def __init__(self, mode, input_dim, output_dim, validate_indices=False,
                 weights_init='truncated_normal', trainable=True, restore=True, name='Embedding'):
        super(Embedding, self).__init__(mode, name)
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.validate_indices = validate_indices
        self.weights_init = weights_init
        self.trainable = trainable
        self.restore = restore

    @property
    def w(self):
        return self._w

    def _build(self, incoming, *args, **kwargs):
        """
        Args:
            2-D Tensor [samples, ids].

        Returns:
            3-D Tensor [samples, embedded_ids, features].
        """
        input_shape = get_shape(incoming)
        assert len(input_shape) == 2, 'Incoming Tensor shape must be 2-D'

        weights_init = getters.get_initializer(self.weights_init)

        self._w = variable('w', shape=[self.input_dim, self.output_dim],
                           initializer=weights_init,
                           trainable=self.trainable, restore=self.restore)
        track(self._w, tf.GraphKeys.LAYER_VARIABLES, self.module_name)
        inference = tf.cast(x=incoming, dtype=tf.int32)
        inference = tf.nn.embedding_lookup(params=self._w, ids=inference,
                                           validate_indices=self.validate_indices)

        track(inference, tf.GraphKeys.LAYER_TENSOR, self.module_name)
        return inference


EMBEDDING_LAYERS = OrderedDict([('Embedding', Embedding)])
