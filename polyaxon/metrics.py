# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.metrics import (
    streaming_true_positives,
    streaming_true_negatives,
    streaming_false_positives,
    streaming_false_negatives,
    streaming_mean,
    streaming_mean_tensor,
    streaming_accuracy,
    streaming_precision,
    streaming_recall,
    streaming_auc,
    streaming_specificity_at_sensitivity,
    streaming_sensitivity_at_specificity,
    streaming_precision_at_thresholds,
    streaming_recall_at_thresholds,
    streaming_sparse_recall_at_k,
    streaming_sparse_precision_at_k,
    streaming_mean_absolute_error,
    streaming_mean_relative_error,
    streaming_mean_squared_error,
    streaming_root_mean_squared_error,
    streaming_covariance,
    streaming_pearson_correlation,
    streaming_mean_cosine_distance,
    streaming_percentage_less,
    streaming_mean_iou,
)

from polyaxon_schemas import metrics


METRICS = OrderedDict([
    (metrics.TruePositivesConfig.IDENTIFIER, streaming_true_positives),
    (metrics.TrueNegativesConfig.IDENTIFIER, streaming_true_negatives),
    (metrics.FalsePositivesConfig.IDENTIFIER, streaming_false_positives),
    (metrics.FalseNegativesConfig.IDENTIFIER, streaming_false_negatives),
    (metrics.MeanConfig.IDENTIFIER, streaming_mean),
    (metrics.MeanTensorConfig.IDENTIFIER, streaming_mean_tensor),
    (metrics.AccuracyConfig.IDENTIFIER, streaming_accuracy),
    (metrics.PrecisionConfig.IDENTIFIER, streaming_precision),
    (metrics.RecallConfig.IDENTIFIER, streaming_recall),
    (metrics.AUCConfig.IDENTIFIER, streaming_auc),
    (metrics.SpecificityAtSensitivityConfig.IDENTIFIER, streaming_specificity_at_sensitivity),
    (metrics.SensitivityAtSpecificityConfig.IDENTIFIER, streaming_sensitivity_at_specificity),
    (metrics.PrecisionAtThresholdsConfig.IDENTIFIER, streaming_precision_at_thresholds),
    (metrics.RecallAtThresholdsConfig.IDENTIFIER, streaming_recall_at_thresholds),
    (metrics.SparseRecallAtKConfig.IDENTIFIER, streaming_sparse_recall_at_k),
    # TODO: this function expects an int64 ==> labels = tf.cast(labels, tf.int64)
    (metrics.SparsePrecisionAtKConfig.IDENTIFIER, streaming_sparse_precision_at_k),
    (metrics.MeanAbsoluteErrorConfig.IDENTIFIER, streaming_mean_absolute_error),
    (metrics.MeanRelativeErrorConfig.IDENTIFIER, streaming_mean_relative_error),
    (metrics.MeanSquaredErrorConfig.IDENTIFIER, streaming_mean_squared_error),
    (metrics.RootMeanSquaredErrorConfig.IDENTIFIER, streaming_root_mean_squared_error),
    (metrics.CovarianceConfig.IDENTIFIER, streaming_covariance),
    (metrics.PearsonCorrelationConfig.IDENTIFIER, streaming_pearson_correlation),
    (metrics.MeanCosineDistanceConfig.IDENTIFIER, streaming_mean_cosine_distance),
    (metrics.PercentageLessConfig.IDENTIFIER, streaming_percentage_less),
    (metrics.MeanIOUConfig.IDENTIFIER, streaming_mean_iou),
])


ARGMAX_METRICS = [
    metrics.TruePositivesConfig.IDENTIFIER,
    metrics.TrueNegativesConfig.IDENTIFIER,
    metrics.FalsePositivesConfig.IDENTIFIER,
    metrics.FalseNegativesConfig.IDENTIFIER,
    metrics.RecallConfig.IDENTIFIER,
    metrics.AUCConfig.IDENTIFIER,
    metrics.AccuracyConfig.IDENTIFIER,
    metrics.PrecisionConfig.IDENTIFIER
]
