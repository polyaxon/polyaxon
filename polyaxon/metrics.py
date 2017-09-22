# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf

from polyaxon_schemas import metrics


METRICS = OrderedDict([
    (metrics.StreamingTruePositivesConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_true_positives),
    (metrics.StreamingTrueNegativesConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_true_negatives),
    (metrics.StreamingFalsePositivesConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_false_positives),
    (metrics.StreamingFalseNegativesConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_false_negatives),
    (metrics.StreamingMeanConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean),
    (metrics.StreamingMeanTensorConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_tensor),
    (metrics.StreamingAccuracyConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_accuracy),
    (metrics.StreamingPrecisionConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_precision),
    (metrics.StreamingRecallConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_recall),
    (metrics.StreamingAUCConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_auc),
    (metrics.StreamingSpecificityAtSensitivityConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_specificity_at_sensitivity),
    (metrics.StreamingSensitivityAtSpecificityConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_sensitivity_at_specificity),
    (metrics.StreamingPrecisionAtThresholdsConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_precision_at_thresholds),
    (metrics.StreamingRecallAtThresholdsConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_recall_at_thresholds),
    (metrics.StreamingSparseRecallAtKConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_sparse_recall_at_k),
    # TODO: this function expects an int64 ==> labels = tf.cast(labels, tf.int64)
    (metrics.StreamingSparsePrecisionAtKConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_sparse_precision_at_k),
    (metrics.StreamingMeanAbsoluteErrorConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_absolute_error),
    (metrics.StreamingMeanRelativeErrorConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_relative_error),
    (metrics.StreamingMeanSquaredErrorConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_squared_error),
    (metrics.StreamingRootMeanSquaredErrorConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_root_mean_squared_error),
    (metrics.StreamingCovarianceConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_covariance),
    (metrics.StreamingPearsonCorrelationConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_pearson_correlation),
    (metrics.StreamingMeanCosineDistanceConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_cosine_distance),
    (metrics.StreamingPercentageLessConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_percentage_less),
    (metrics.StreamingMeanIOUConfig.IDENTIFIER,
     tf.contrib.metrics.streaming_mean_iou),
])


ARGMAX_METRICS = [
    metrics.StreamingTruePositivesConfig.IDENTIFIER,
    metrics.StreamingTrueNegativesConfig.IDENTIFIER,
    metrics.StreamingFalsePositivesConfig.IDENTIFIER,
    metrics.StreamingFalseNegativesConfig.IDENTIFIER,
    metrics.StreamingRecallConfig.IDENTIFIER,
    metrics.StreamingAUCConfig.IDENTIFIER,
    metrics.StreamingAccuracyConfig.IDENTIFIER,
    metrics.StreamingPrecisionConfig.IDENTIFIER
]
