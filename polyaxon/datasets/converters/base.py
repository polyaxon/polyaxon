# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf


class BaseConverter(object):
    @staticmethod
    def to_int64_feature(values):
        """Returns a TF-Feature of int64s.

        Args:
            values: A scalar or list of values.

        Returns:
            a TF-Feature.
        """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=values))

    @staticmethod
    def to_bytes_feature(values):
        """Returns a TF-Feature of bytes.

        Args:
            values: A string.

        Returns:
            a TF-Feature.
        """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=values))

    @staticmethod
    def to_float_feature(values):
        """Returns a TF-Feature of floats.

        Args:
            values: A string.

        Returns:
            a TF-Feature.
        """
        if not isinstance(values, list):
            values = [values]
        return tf.train.Feature(float_list=tf.train.FloatList(value=values))

    @classmethod
    def to_feature(cls, value, value_type):
        if value_type == 'int':
            return cls.to_int64_feature(value)
        if value_type == 'float':
            return cls.to_float_feature(value)
        if value_type == 'bytes':
            return cls.to_bytes_feature(value)

        raise TypeError("value type: `{}` is not supported.".format(value_type))

    @classmethod
    def to_sequence_feature(cls, sequence, sequence_type):
        """Returns a FeatureList based on a list fo features of type sequence_type

        Args:
            sequence: list of values
            sequence_type: type of the sequence.

        Returns:
            list of TF-FeatureList
        """
        if sequence_type == 'int':
            feature_list = [cls.to_int64_feature(i) for i in sequence]
        elif sequence_type == 'float':
            feature_list = [cls.to_float_feature(i) for i in sequence]
        elif sequence_type == 'bytes':
            feature_list = [cls.to_bytes_feature(i) for i in sequence]
        else:
            raise TypeError("sequence type: `{}` is not supported.".format(sequence_type))

        return tf.train.FeatureList(feature=feature_list)
