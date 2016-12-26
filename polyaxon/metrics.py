# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon.libs.utils import get_name_scope, track


def check_metric_data(y_pred, y_true):
    if not isinstance(y_true, tf.Tensor):
        raise ValueError("mean_accuracy 'input' argument only accepts type "
                         "Tensor, '" + str(type(input)) + "' given.")
    y_true = tf.cast(y_true, y_true.dtype)
    y_true.get_shape().assert_is_compatible_with(y_pred.get_shape())


def built_metric(fct, name, scope, collect):
    """ Builds the metric function.

    Args:
        fct: the metric function to build.
        name: operation name.
        scope: operation scope.
        collect: whether to collect this metric under the metric collection.
    """
    def metric(y_pred, y_true):
        """
        Args:
            y_pred: `Tensor`
            y_true: `Tensor`

        Returns:
            `Float`. The calculated metric.
        """
        check_metric_data(y_pred, y_true)
        with get_name_scope(name, scope):
            x = fct(y_pred, y_true)
            if collect:
                track(x, tf.GraphKeys.METRICS)
            return x
    return metric


def accuracy(name='Accuracy', scope=None, collect=False):
    """ Computes the accuracy.

    An op that calculates mean accuracy:
        * y_pred are y_True are both one-hot encoded. (categorical accuracy)
        * y_pred are logits are binary encoded (and represented as int32). (binary accuracy)


    Examples:
        ```python
        input_data = placeholder(shape=[None, 784])
        y_pred = my_network(input_data) # Apply some ops
        y_true = placeholder(shape=[None, 10]) # Labels
        accuracy_op = accuracy(y_pred, y_true)

        # Calculate accuracy by feeding data X and labels Y
        accuracy_op = sess.run(accuracy_op, feed_dict={input_data: X, y_true: Y})
        ```

    Args:
        scope: scope to add the op to.
        name: name of the op.
        collect: add to metrics collection.

    Returns:
        `Float`. The mean accuracy.
    """
    def inner_metric(y_pred, y_true):
        def categorical_accuracy(y_pred, y_true):
            correct_pred = tf.equal(x=tf.argmax(input=y_pred, axis=1), y=tf.argmax(input=y_true, axis=1))
            return tf.reduce_mean(input_tensor=tf.cast(x=correct_pred, dtype=tf.float32))

        def binary_accuracy(y_pred, y_true):
            y_pred = tf.cast(x=tf.greater(x=y_pred, y=0), dtype=tf.float32)
            correct_pred = tf.equal(x=y_pred, y=tf.cast(x=y_true, dtype=tf.float32))
            return tf.reduce_mean(input_tensor=tf.cast(x=correct_pred, dtype=tf.float32))

        y_pred_shape = y_pred.get_shape()
        is_binary = len(y_pred_shape) == 1 or (len(y_pred_shape) == 2 and int(y_pred_shape[1]) == 1)
        return (binary_accuracy(y_pred, y_true) if is_binary
                else categorical_accuracy(y_pred, y_true))

    return built_metric(inner_metric, name, scope, collect)


def top_k(k=1, name='TopK', scope=None, collect=False):
    """ top_k_op.

    An op that calculates top-k mean accuracy.

    Examples:
        ```python
        input_data = placeholder(shape=[None, 784])
        y_pred = my_network(input_data) # Apply some ops
        y_true = placeholder(shape=[None, 10]) # Labels
        top3_op = top_k(y_pred, y_true, 3)

        # Calculate Top-3 accuracy by feeding data X and labels Y
        top3_accuracy = sess.run(top3_op, feed_dict={input_data: X, y_true: Y})
        ```

    Args:
        k: `int`. Number of top elements to look at for computing precision.
        scope: scope to add the op to.
        name: name of the op.
        collect: add to metrics collection.

    Returns:
        `Float`. The top-k mean accuracy.
    """

    def inner_metric(y_pred, y_true):
        y_true = tf.cast(x=y_true, dtype=tf.int32)
        correct_pred = tf.nn.in_top_k(predictions=y_pred, targets=tf.argmax(y_true, 1), k=k)
        return tf.reduce_mean(input_tensor=tf.cast(x=correct_pred, dtype=tf.float32))

    return built_metric(inner_metric, name, scope, collect)


def std_error(name='StandardError', scope=None, collect=False):
    """ standard error.

    An op that calculates the standard error.

    Examples:
        ```python
        input_data = placeholder(shape=[None, 784])
        y_pred = my_network(input_data) # Apply some ops
        y_true = placeholder(shape=[None, 10]) # Labels
        stderr = std_error(y_pred, y_true)

        # Calculate standard error by feeding data X and labels Y
        std_error = sess.run(stderr_op, feed_dict={input_data: X, y_true: Y})
        ```

    Args:
        scope: scope to add the op to.
        name: name of the op.
        collect: add to metrics collection.

    Returns:
        `Float`. The standard error.
    """

    def inner_metric(y_pred, y_true):
        a = tf.reduce_sum(input_tensor=tf.square(y_pred))
        b = tf.reduce_sum(input_tensor=tf.square(y_true))
        return tf.div(x=a, y=b)

    return built_metric(inner_metric, name, scope, collect)


METRICS = {
    'accuracy': accuracy,
    'top_k': top_k,
    'std_error': std_error
}


EVAL_METRICS = {
    'streaming_true_positives': tf.contrib.metrics.streaming_true_positives,
    'streaming_true_negatives': tf.contrib.metrics.streaming_true_negatives,
    'streaming_false_positives': tf.contrib.metrics.streaming_false_positives,
    'streaming_false_negatives': tf.contrib.metrics.streaming_false_negatives,
    'streaming_mean': tf.contrib.metrics.streaming_mean,
    'streaming_mean_tensor': tf.contrib.metrics.streaming_mean_tensor,
    'streaming_accuracy': tf.contrib.metrics.streaming_accuracy,
    'streaming_precision': tf.contrib.metrics.streaming_precision,
    'streaming_recall': tf.contrib.metrics.streaming_recall,
    'streaming_auc': tf.contrib.metrics.streaming_auc,
    'streaming_specificity_at_sensitivity': tf.contrib.metrics.streaming_specificity_at_sensitivity,
    'streaming_sensitivity_at_specificity': tf.contrib.metrics.streaming_sensitivity_at_specificity,
    'streaming_precision_at_thresholds': tf.contrib.metrics.streaming_precision_at_thresholds,
    'streaming_recall_at_thresholds': tf.contrib.metrics.streaming_recall_at_thresholds,
    'streaming_sparse_recall_at_k': tf.contrib.metrics.streaming_sparse_recall_at_k,
    'streaming_sparse_precision_at_k': tf.contrib.metrics.streaming_sparse_precision_at_k,
    'streaming_sparse_precision_at_top_k': tf.contrib.metrics.streaming_sparse_precision_at_top_k,
    'streaming_sparse_average_precision_at_k': tf.contrib.metrics.streaming_sparse_average_precision_at_k,
    'streaming_sparse_average_precision_at_top_k': tf.contrib.metrics.streaming_sparse_average_precision_at_top_k,
    'streaming_mean_absolute_error': tf.contrib.metrics.streaming_mean_absolute_error,
    'streaming_mean_relative_error': tf.contrib.metrics.streaming_mean_relative_error,
    'streaming_mean_squared_error': tf.contrib.metrics.streaming_mean_squared_error,
    'streaming_root_mean_squared_error': tf.contrib.metrics.streaming_root_mean_squared_error,
    'streaming_covariance': tf.contrib.metrics.streaming_covariance,
    'streaming_pearson_correlation': tf.contrib.metrics.streaming_pearson_correlation,
    'streaming_mean_cosine_distance': tf.contrib.metrics.streaming_mean_cosine_distance,
    'streaming_percentage_less': tf.contrib.metrics.streaming_percentage_less,
    'streaming_mean_iou': tf.contrib.metrics.streaming_mean_iou
}
