#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from polyaxon import tracking
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.utils.np_utils import sanitize_dict

try:
    from sklearn.base import is_classifier, is_regressor
    from sklearn.metrics import (
        accuracy_score,
        explained_variance_score,
        f1_score,
        max_error,
        mean_absolute_error,
        precision_recall_fscore_support,
        r2_score,
    )
except ImportError:
    raise PolyaxonClientException(
        "sklearn is required to use scikit polyaxon's loggers"
    )


def _log_test_predictions(run, y_test, y_pred=None, nrows=1000):
    try:
        import pandas as pd
    except ImportError:
        return

    # single output
    if len(y_pred.shape) == 1:
        df = pd.DataFrame(data={"y_true": y_test, "y_pred": y_pred})
        run.log_dataframe(df=df.head(nrows), name="test_predictions")

    # multi output
    if len(y_pred.shape) == 2:
        df = pd.DataFrame()
        for j in range(y_pred.shape[1]):
            df["y_test_output_{}".format(j)] = y_test[:, j]
            df["y_pred_output_{}".format(j)] = y_pred[:, j]
        run.log_dataframe(df=df.head(nrows), name="test_predictions")


def _log_test_preds_proba(run, classifier, X_test, nrows=1000):
    try:
        import pandas as pd
    except ImportError:
        return

    try:
        y_pred_proba = classifier.predict_proba(X_test)
    except Exception as e:
        print(
            "This classifier does not provide predictions probabilities. Error: {}".format(
                e
            )
        )
        return

    df = pd.DataFrame(data=y_pred_proba, columns=classifier.classes_)
    run.log_dataframe(df=df.head(nrows), name="test_proba_predictions")


def log_regressor(regressor, X_test, y_test, nrows=1000, run=None):
    assert is_regressor(regressor), "regressor should be sklearn regressor."

    run = tracking.get_or_create_run(run)

    run.log_inputs(**regressor.get_params())

    y_pred = regressor.predict(X_test)

    # single output
    results = {}
    if len(y_pred.shape) == 1:
        results["evs"] = explained_variance_score(y_test, y_pred)
        results["me"] = max_error(y_test, y_pred)
        results["mae"] = mean_absolute_error(y_test, y_pred)
        results["r2"] = r2_score(y_test, y_pred)
    # multi output
    if len(y_pred.shape) == 2:
        results["r2"] = regressor.score(X_test, y_test)
    run.log_metrics(**results)

    _log_test_predictions(run, y_test, y_pred=y_pred, nrows=nrows)


def log_classifier(classifier, X_test, y_test, nrows=1000, run=None):
    assert is_classifier(classifier), "classifier should be sklearn classifier."

    run = tracking.get_or_create_run(run)

    run.log_inputs(**sanitize_dict(classifier.get_params()))

    _log_test_preds_proba(run, classifier, X_test, nrows=nrows)

    y_pred = classifier.predict(X_test)

    results = {}
    for metric_name, values in zip(
        ["precision", "recall", "fbeta_score", "support"],
        precision_recall_fscore_support(y_test, y_pred),
    ):
        for i, value in enumerate(values):
            results["{}_class_{}_test".format(metric_name, i)] = value
    results["accuracy"] = accuracy_score(y_test, y_pred)
    results["f1"] = f1_score(y_pred, y_pred, average="weighted")
    run.log_metrics(**results)
    _log_test_predictions(run, y_test, y_pred=y_pred, nrows=nrows)
