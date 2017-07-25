# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import sys

from six.moves import xrange
from collections import Mapping

import tensorflow as tf

from polyaxon.datasets.converters.base import BaseConverter


class SequenceToTFExampleConverter(BaseConverter):
    """Converts images to a TFRecords of TF-Example protos.

    Each record is TF-Example protocol buffer which contain a single image and label.

    Args:
        sequence_features_types: `dict`. A mapping between the sequence features and their types.
        context_features_types: `dict`. A mapping between the context features and their types.
        store_filenames: `bool`. If `True` the filename of the image will be stored as a feature.
    """
    def __init__(self, sequence_features_types, context_features_types=None, store_filenames=False):
        if not isinstance(sequence_features_types, Mapping):
            raise ValueError("`sequence_features_types` must be a mapping "
                             "form feature name to a type.")
        if context_features_types is not None and not isinstance(context_features_types, Mapping):
            raise ValueError("`context_features_types` must be a mapping "
                             "form feature name to a type.")

        self.sequence_features_types = sequence_features_types
        self.context_features_types = context_features_types
        self.store_filenames = store_filenames

    def get_meta_data(self):
        return {
            'sequence_features_types': self.sequence_features_types,
            'context_features_types': self.context_features_types
        }

    def _create_sequence_features(self, sequence_features):
        feature_list = {}
        for name, sequence in sequence_features.items():
            feature_type = self.sequence_features_types[name]
            feature_list[name] = self.to_sequence_feature(sequence, feature_type)

        return tf.train.FeatureLists(feature_list=feature_list)

    def _create_context_features(self, context_features, filename=None):
        context = {}
        for name, value in context_features.items():
            feature_type = self.context_features_types[name]
            context[name] = self.to_feature(value, feature_type)

        if self.store_filenames and filename:
            filename_feature = self.to_bytes_feature(tf.compat.as_bytes(os.path.basename(filename)))
            context['filename'] = filename_feature
        return context

    def create_example(self, sequence_features, context_features=None, filename=None):
        """

        Args:
            sequence_features: `dict`. A mapping from feature names to sequences
            context_features: `dict`. A mapping from feature names to values.
            filename: `str`. File name where the data was extracted from.

        Returns:
            `TFSequenceExample`
        """
        if not isinstance(sequence_features, Mapping):
            raise ValueError("`sequence_features` must a mapping form feature name to a type.")
        if context_features is not None and not isinstance(context_features, Mapping):
            raise ValueError("`context_features` must a mapping form feature name to a type.")

        feature_lists = self._create_sequence_features(sequence_features)
        if context_features:
            context = self._create_context_features(context_features, filename)
            return tf.train.SequenceExample(feature_lists=feature_lists,
                                            context=tf.train.Features(feature=context))

        return tf.train.SequenceExample(feature_lists=feature_lists)

    def convert(self, session, writer, sequence_features_list, context_features_list,
                total_num_items, start_index=0, filenames=None):

        if self.store_filenames and not filenames:
            raise ValueError('`filenames` is required to store the filename in TF-Example.'
                             'Either provide a list of `filenames` or '
                             'set `store_filenames` to `False`')

        for i in xrange(start_index, len(sequence_features_list)):
            sys.stdout.write('\r>> Converting sequence %d/%d' % (i + 1, total_num_items))
            sys.stdout.flush()

            example = self.create_example(
                sequence_features_list[i],
                context_features_list[i] if self.context_features_types is not None else None,
                filenames[i] if self.store_filenames else None)
            writer.write(example.SerializeToString())
