# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn
from tensorflow.python.estimator.inputs.pandas_io import pandas_input_fn

from polyaxon.libs import getters
from polyaxon.libs.configs import InputDataConfig


def create_input_data_fn(mode, pipeline_config, scope=None, input_type=None, x=None, y=None):
    """Creates an input data function that can be used with estimators.
    Note that you must pass "factory functions" for both the data provider and
    featurizer to ensure that everything will be created in  the same graph.

    Args:
        mode: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
        pipeline_config: the configuration to create a Pipeline instance.
        scope: `str`. scope to use for this input data block.
        input_type: `str`. The type of the input, values: `NUMPY`, `PANDAS`.
                    If `None`, will create a function based on the pipeline config.
        x: `np.ndarray` or `np.Dataframe` or `None`.
        y: `np.ndarray` or `None`.

    Returns:
        An input function that returns `(feature_batch, labels_batch)`
        tuples when called.
    """
    pipeline_config = pipeline_config

    if input_type == InputDataConfig.NUMPY:
        # setup_train_data_feeder
        return numpy_input_fn(x, y,
                              batch_size=pipeline_config.batch_size,
                              num_epochs=pipeline_config.num_epochs,
                              shuffle=pipeline_config.shuffle,
                              num_threads=pipeline_config.num_threads)

    if input_type == InputDataConfig.PANDAS:
        # setup_train_data_feeder
        return pandas_input_fn(x, y,
                               batch_size=pipeline_config.batch_size,
                               num_epochs=pipeline_config.num_epochs,
                               shuffle=pipeline_config.shuffle,
                               num_threads=pipeline_config.num_threads)

    def input_fn():
        """Creates features and labels."""
        pipeline_params = pipeline_config.to_dict()
        batch_size = pipeline_params.pop('batch_size', None)
        dynamic_pad = pipeline_params.pop('dynamic_pad', None)
        capacity = pipeline_params.pop('capacity', None)
        del pipeline_params['num_threads']
        del pipeline_params['min_after_dequeue']
        allow_smaller_final_batch = pipeline_params.pop('allow_smaller_final_batch', None)
        bucket_boundaries = pipeline_params.pop('bucket_boundaries', None)

        pipeline = getters.get_pipeline(
            mode=mode, module=pipeline_config.IDENTIFIER, **pipeline_params)

        with tf.variable_scope(scope or 'input_fn'):
            data_provider = pipeline.make_data_provider()
            features_and_labels = pipeline.read_from_data_provider(data_provider)
            # call pipeline processors
            features_and_labels = pipeline(features_and_labels, None)

            if bucket_boundaries:
                _, batch = tf.contrib.training.bucket_by_sequence_length(
                    input_length=features_and_labels['source_len'],
                    bucket_boundaries=bucket_boundaries,
                    tensors=features_and_labels,
                    batch_size=batch_size,
                    keep_input=features_and_labels['source_len'] >= 1,
                    dynamic_pad=dynamic_pad,
                    capacity=capacity,
                    allow_smaller_final_batch=allow_smaller_final_batch,
                    name='bucket_queue')
            else:
                batch = tf.train.batch(
                    tensors=features_and_labels,
                    enqueue_many=False,
                    batch_size=batch_size,
                    dynamic_pad=dynamic_pad,
                    capacity=capacity,
                    allow_smaller_final_batch=allow_smaller_final_batch,
                    name='batch_queue')

            # Separate features and labels
            features_batch = {k: batch[k] for k in pipeline.feature_keys}
            if set(batch.keys()).intersection(pipeline.label_keys):
                labels_batch = {k: batch[k] for k in pipeline.label_keys}
            else:
                labels_batch = None

            return features_batch, labels_batch

    return input_fn
