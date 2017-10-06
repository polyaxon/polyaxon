# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import six

import tensorflow as tf

from tensorflow.python.ops import array_ops


@six.add_metaclass(abc.ABCMeta)
class DataDecoder(object):
    """An abstract class which is used to decode data for a provider.

    (A mirror to tf.slim.data DataDecoder)
    """

    @abc.abstractmethod
    def decode(self, data, items):
        """Decodes the data to returns the tensors specified by the list of items.

    Args:
      data: A possibly encoded data format.
      items: A list of strings, each of which indicate a particular data type.

    Returns:
      A list of `Tensors`, whose length matches the length of `items`, where
      each `Tensor` corresponds to each item.

    Raises:
      ValueError: If any of the items cannot be satisfied.
    """
        pass

    @abc.abstractmethod
    def list_items(self):
        """Lists the names of the items that the decoder can decode.

    Returns:
      A list of string names.
    """
        pass


class TFExampleDecoder(DataDecoder):
    """A decoder for TensorFlow Examples.
    (A mirror to tf.slim.data TFExampleDecoder)

    Decoding Example proto buffers is comprised of two stages: (1) Example parsing
    and (2) tensor manipulation.

    In the first stage, the tf.parse_example function is called with a list of
    FixedLenFeatures and SparseLenFeatures. These instances tell TF how to parse
    the example. The output of this stage is a set of tensors.

    In the second stage, the resulting tensors are manipulated to provide the
    requested 'item' tensors.

    To perform this decoding operation, an ExampleDecoder is given a list of
    ItemHandlers. Each ItemHandler indicates the set of features for stage 1 and
    contains the instructions for post_processing its tensors for stage 2.
    """

    def __init__(self, keys_to_features, items_to_handlers):
        """Constructs the decoder.

        Args:
            keys_to_features: a dictionary from TF-Example keys to either
                tf.VarLenFeature or tf.FixedLenFeature instances.
            items_to_handlers: a dictionary from items (strings) to ItemHandler instances.
            Note that the ItemHandler's are provided the keys that they use
            to return the final item Tensors.
        """
        self._keys_to_features = keys_to_features
        self._items_to_handlers = items_to_handlers

    def list_items(self):
        """See base class."""
        return list(self._items_to_handlers.keys())

    def decode(self, data, items=None):
        """Decodes the given serialized TF-example.

        Args:
            data: a serialized TF-example tensor.
            items: the list of items to decode. These must be a subset of the item
                keys in self._items_to_handlers. If `items` is left as None, then all
                of the items in self._items_to_handlers are decoded.

        Returns:
            the decoded items, a list of tensor.
        """
        example = tf.parse_single_example(data, self._keys_to_features)

        # Reshape non-sparse elements just once:
        for k in self._keys_to_features:
            v = self._keys_to_features[k]
            if isinstance(v, tf.FixedLenFeature):
                example[k] = array_ops.reshape(example[k], v.shape)

        if not items:
            items = self._items_to_handlers.keys()

        outputs = []
        for item in items:
            handler = self._items_to_handlers[item]
            keys_to_tensors = {key: example[key] for key in handler.keys}
            outputs.append(handler.tensors_to_item(keys_to_tensors))
        return outputs


class SplitTokensDecoder(DataDecoder):
    """A DataDecoder that splits a string tensor into individual tokens and
    returns the tokens and the length.
    Optionally prepends or appends special tokens.

    Args:
        delimiter: Delimiter to split on. Must be a single character.
        tokens_feature_name: A descriptive feature name for the token values
        length_feature_name: A descriptive feature name for the length value
    """

    def __init__(self,
                 delimiter=" ",
                 tokens_feature_name="tokens",
                 length_feature_name="length",
                 prepend_token=None,
                 append_token=None):
        self.delimiter = delimiter
        self.tokens_feature_name = tokens_feature_name
        self.length_feature_name = length_feature_name
        self.prepend_token = prepend_token
        self.append_token = append_token

    def decode(self, data, items):
        decoded_items = {}

        # Split tokens
        tokens = tf.string_split([data], delimiter=self.delimiter).values

        # Optionally prepend a special token
        if self.prepend_token is not None:
            tokens = tf.concat([[self.prepend_token], tokens], 0)

        # Optionally append a special token
        if self.append_token is not None:
            tokens = tf.concat([tokens, [self.append_token]], 0)

        decoded_items[self.length_feature_name] = tf.size(tokens)
        decoded_items[self.tokens_feature_name] = tokens
        return [decoded_items[_] for _ in items]

    def list_items(self):
        return [self.tokens_feature_name, self.length_feature_name]


class TFSequenceExampleDecoder(DataDecoder):
    """A decoder for TensorFlow Sequence Examples.

    Decoding Example proto buffers is comprised of two stages: (1) Example parsing
    and (2) tensor manipulation.

    In the first stage, the tf.parse_single_sequence_example function is called with a list of
    FixedLenFeatures, SparseLenFeatures, and FixedLenSequenceFeature.
    These instances tell TF how to parse the example. The output of this stage is a set of tensors.
    In the second stage, the resulting tensors are manipulated to provide the
    requested 'item' tensors.
    To perform this decoding operation, an ExampleDecoder is given a list of
    ItemHandlers. Each ItemHandler indicates the set of features for stage 1 and
    contains the instructions for post_processing its tensors for stage 2.
    """

    def __init__(self, context_keys_to_features, sequence_keys_to_features, items_to_handlers):
        """Constructs the decoder.
        Args:
          keys_to_features: a dictionary from TF-Example keys to either
            tf.VarLenFeature or tf.FixedLenFeature instances. See tensorflow's
            parsing_ops.py.
          items_to_handlers: a dictionary from items (strings) to ItemHandler
            instances. Note that the ItemHandler's are provided the keys that they
            use to return the final item Tensors.
        """
        self._context_keys_to_features = context_keys_to_features
        self._sequence_keys_to_features = sequence_keys_to_features
        self._items_to_handlers = items_to_handlers

    def list_items(self):
        """See base class."""
        return list(self._items_to_handlers.keys())

    def decode(self, data, items=None):
        """Decodes the given serialized TF-example.
        Args:
          data: a serialized TF-example tensor.
          items: the list of items to decode. These must be a subset of the item
            keys in self._items_to_handlers. If `items` is left as None, then all
            of the items in self._items_to_handlers are decoded.
        Returns:
          the decoded items, a list of tensor.
        """
        context, sequence = tf.parse_single_sequence_example(
            data, self._context_keys_to_features, self._sequence_keys_to_features)

        # Merge context and sequence features
        example = {}
        example.update(context)
        example.update(sequence)

        all_features = {}
        all_features.update(self._context_keys_to_features)
        all_features.update(self._sequence_keys_to_features)

        # Reshape non-sparse elements just once:
        for k, value in all_features.items():
            if isinstance(value, tf.FixedLenFeature):
                example[k] = tf.reshape(example[k], value.shape)

        if not items:
            items = self._items_to_handlers.keys()

        outputs = []
        for item in items:
            handler = self._items_to_handlers[item]
            keys_to_tensors = {key: example[key] for key in handler.keys}
            outputs.append(handler.tensors_to_item(keys_to_tensors))
        return outputs
