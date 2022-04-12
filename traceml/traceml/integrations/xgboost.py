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
import ujson

from traceml import tracking
from traceml.exceptions import TracemlException
from traceml.logger import logger

try:
    import xgboost as xgb

    from xgboost import Booster
except ImportError:
    raise TracemlException("xgboost is required to use the tracking callback")


def _get_cv(model):
    return getattr(model, "cvfolds", False)


def _log_importance(run, model, model_folds, max_num_features, **kwargs):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Please install matplotlib to log importance")

    if model_folds:
        for i, fold in enumerate(model_folds):
            importance = xgb.plot_importance(
                fold.bst, max_num_features=max_num_features, **kwargs
            )
            run.log_mpl_plotly_chart(
                name="feature_importance", figure=importance.figure, step=i
            )
    else:
        importance = xgb.plot_importance(
            model, max_num_features=max_num_features, **kwargs
        )
        run.log_mpl_plotly_chart(name="feature_importance", figure=importance.figure)
    plt.close("all")


def _log_model(run, model, model_folds):
    def _save(file_model, file_name):
        asset_path = run.get_outputs_path(file_name)
        file_model.save_model(asset_path)
        run.log_model_ref(asset_path, framework="xgboost")

    if model_folds:
        for i, cvpack in enumerate(model_folds):
            _save(cvpack.bst, "model-{}".format(i))
    else:  # train case
        _save(model, "model")


def callback(
    log_model: bool = True,
    log_importance: bool = True,
    max_num_features: int = None,
    run: "Run" = None,
):
    run = tracking.get_or_create_run(run)

    def callback(env):
        # Log metrics after iteration
        metrics = {}
        for item in env.evaluation_result_list:
            if len(item) == 2:  # train case
                metrics[item[0]] = item[1]
            if len(item) == 3:  # cv case
                metrics["{}-mean".format(item[0])] = item[1]
                metrics["{}-std".format(item[0])] = item[2]
        run.log_metrics(
            **metrics,
            step=env.iteration,
        )

        model = getattr(env, "model")
        model_folds = _get_cv(env)

        # Log booster, end of training
        if log_model:
            _log_model(run=run, model=model, model_folds=model_folds)

        # Log feature importance, end of training
        if env.iteration + 1 == env.end_iteration and log_importance:
            try:
                _log_importance(
                    run,
                    model=model,
                    model_folds=model_folds,
                    max_num_features=max_num_features,
                )
            except Exception as e:
                logger.info("Failed logging feature importance %s", e)

    return callback


class Callback(xgb.callback.TrainingCallback):
    def __init__(
        self,
        run: "Run" = None,
        log_model: bool = True,
        log_importance: bool = True,
        importance_type: str = "gain",
        max_num_features: int = None,
    ):

        self.log_model: bool = log_model
        self.log_importance: bool = log_importance
        self.importance_type: str = importance_type
        self.max_num_features: int = max_num_features
        self.run = tracking.get_or_create_run(run)

    def after_training(self, model: Booster) -> Booster:
        model_folds = _get_cv(model)

        if self.log_model:
            _log_model(run=self.run, model=model, model_folds=model_folds)

        if self.log_importance:
            _log_importance(
                self.run,
                model=model,
                model_folds=model_folds,
                max_num_features=self.max_num_features,
            )

        if model_folds:
            config = {}
            for i, fold in enumerate(model_folds):
                config["fold_{}_config".format(i)] = ujson.loads(fold.bst.save_config())
            if config:
                self.run.log_inputs(**config)
        else:
            self.run.log_inputs(config=ujson.loads(model.save_config()))
            outputs = {}
            if "best_score" in model.attributes().keys():
                outputs["best_score"] = model.attributes()["best_score"]
            if "best_iteration" in model.attributes().keys():
                outputs["best_iteration"] = model.attributes()["best_iteration"]
            self.run.log_outputs(**outputs)

        return model

    def after_iteration(self, model: Booster, epoch: int, evals_log: dict) -> bool:
        metrics = {}
        for stage, metrics_dict in evals_log.items():
            for metric_name, metric_values in evals_log[stage].items():
                if _get_cv(model):
                    mean, std = metric_values[-1]
                    metrics["{}-{}-mean".format(stage, metric_name)] = mean
                    metrics["{}-{}-std".format(stage, metric_name)] = std
                else:
                    metrics["{}-{}".format(stage, metric_name)] = metric_values[-1]

        if metrics:
            self.run.log_metrics(step=epoch, **metrics)

        return False
