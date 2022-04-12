#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List

from polyaxon.constants.globals import UNKNOWN
from polyaxon.utils.np_utils import to_np
from traceml.artifacts import V1ArtifactKind
from traceml.events import (
    LoggedEventSpec,
    V1Event,
    V1EventConfusionMatrix,
    V1EventCurve,
    V1EventCurveKind,
    V1EventHistogram,
)
from traceml.logger import logger
from traceml.processors.errors import NUMPY_ERROR_MESSAGE, SKLEARN_ERROR_MESSAGE

try:
    import numpy as np
except ImportError:
    np = None


def metric(value):
    if isinstance(value, float):
        return value

    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    value = to_np(value)
    assert value.squeeze().ndim == 0, "scalar should be 0D"
    return float(value)


def histogram(values, bins, max_bins=None):
    if not np:
        logger.warning(NUMPY_ERROR_MESSAGE)
        return UNKNOWN

    values = to_np(values).astype(float)

    if values.size == 0:
        raise ValueError("The input has no element.")
    values = values.reshape(-1)
    values, counts = np.histogram(values, bins=bins)

    if counts.size == 0:
        logger.warning("Tracking an empty histogram")
        return UNKNOWN

    return np_histogram(values=values, counts=counts, max_bins=max_bins)


def np_histogram(values, counts, max_bins=None):
    try:
        values = values.tolist()
        counts = counts.tolist()
    except:  # noqa
        pass
    max_bins = max_bins or 512
    values_len = len(values)
    counts_len = len(counts)
    if values_len > max_bins:
        raise ValueError(
            "The maximum bins for a histogram is {}, received {}".format(
                max_bins, values_len
            )
        )
    if values_len + 1 != counts_len:
        raise ValueError("len(hist.values) must be len(hist.counts) + 1")
    return V1EventHistogram(values=values, counts=counts)


def roc_auc_curve(fpr, tpr, auc=None):
    return V1EventCurve(
        kind=V1EventCurveKind.ROC,
        x=fpr,
        y=tpr,
        annotation=str(auc) if auc else None,
    )


def sklearn_roc_auc_curve(y_preds, y_targets, pos_label=None):
    try:
        from sklearn.metrics import auc, roc_curve
    except ImportError:
        logger.warning(SKLEARN_ERROR_MESSAGE)

    try:
        y_true = y_targets.numpy()
    except AttributeError:
        y_true = y_targets
    try:
        y_pred = y_preds.numpy()
    except AttributeError:
        y_pred = y_preds
    fpr, tpr, _ = roc_curve(y_true, y_pred, pos_label=pos_label)
    auc_score = auc(fpr, tpr)
    return V1EventCurve(
        kind=V1EventCurveKind.ROC,
        x=fpr,
        y=tpr,
        annotation=str(auc_score),
    )


def pr_curve(precision, recall, average_precision=None):
    return V1EventCurve(
        kind=V1EventCurveKind.PR,
        x=precision,
        y=recall,
        annotation=str(average_precision) if average_precision else None,
    )


def sklearn_pr_curve(y_preds, y_targets, pos_label=None):
    try:
        from sklearn.metrics import average_precision_score, precision_recall_curve
    except ImportError:
        logger.warning(SKLEARN_ERROR_MESSAGE)

    try:
        y_true = y_targets.numpy()
    except AttributeError:
        y_true = y_targets
    try:
        y_pred = y_preds.numpy()
    except AttributeError:
        y_pred = y_preds

    precision, recall, _ = precision_recall_curve(y_true, y_pred, pos_label=pos_label)
    ap = average_precision_score(y_true, y_pred)
    return V1EventCurve(
        kind=V1EventCurveKind.PR,
        x=precision,
        y=recall,
        annotation=str(ap),
    )


def curve(x, y, annotation=None):
    return V1EventCurve(
        kind=V1EventCurveKind.CUSTOM,
        x=x,
        y=y,
        annotation=str(annotation) if annotation else None,
    )


def confusion_matrix(x, y, z):
    if hasattr(x, "tolist"):
        x = x.tolist()
    if hasattr(x, "tolist"):
        y = y.tolist()
    if hasattr(x, "tolist"):
        z = z.tolist()
    try:
        x_len = len(x)
        y_len = len(y)
        z_len = len(z)
        if x_len != y_len or x_len != z_len:
            raise ValueError(
                "Received invalid data for confusion matrix. "
                "All arrays must have the same structure: "
                "[len(x): {}, len(y): {}, len(z): {}]".format(
                    x_len,
                    y_len,
                    z_len,
                )
            )
        zi_len = [len(zi) for zi in z]
        if len(set(zi_len)) != 1 or zi_len[0] != z_len:
            raise ValueError(
                "Received invalid data for confusion matrix. "
                "Current structure: [len(x): {}, len(y): {}, len(z): {}]. "
                "The z array has different nested structures: {}".format(
                    x_len, y_len, z_len, zi_len
                )
            )
    except Exception as e:  # noqa
        raise ValueError(
            "Received invalid data for confusion matrix. Error {}".format(e)
        )
    return V1EventConfusionMatrix(
        x=x,
        y=y,
        z=z,
    )


def metrics_dict_to_list(metrics: Dict) -> List:
    results = []
    for k, v in metrics.items():
        results.append(
            LoggedEventSpec(
                name=k,
                kind=V1ArtifactKind.METRIC,
                event=V1Event.make(metric=v),
            )
        )
    return results
