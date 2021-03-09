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

try:
    import xgboost as xgb
except ImportError:
    raise PolyaxonClientException("xgboost is required to use polyaxon_callback")


def polyaxon_callback(
    log_model: bool = True,
    log_importance: bool = True,
    max_num_features: int = None,
    run=None,
):
    run = tracking.get_or_create_run(run)

    def _log_model(booster, name):
        asset_path = run.get_outputs_path(name)
        booster.save_model(asset_path)
        run.log_model_ref(asset_path, framework="xgboost")

    def _log_importance(booster, max_num_features, **kwargs):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("Please install matplotlib to log importance")
        importance = xgb.plot_importance(
            booster, max_num_features=max_num_features, **kwargs
        )
        run.log_mpl_plotly_chart(name="feature_importance", figure=importance.figure)
        plt.close("all")

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

        # Log booster, end of training
        if env.iteration + 1 == env.end_iteration and log_model:
            if env.cvfolds:  # cv case
                for i, cvpack in enumerate(env.cvfolds):
                    _log_model(cvpack.bst, "cv-fold-{}-bst.model".format(i))
            else:  # train case
                _log_model(env.model, "bst.model")

        # Log feature importance, end of training
        if env.iteration + 1 == env.end_iteration and log_importance:
            if env.cvfolds:  # cv case
                for i, cvpack in enumerate(env.cvfolds):
                    _log_importance(
                        cvpack.bst, max_num_features, title="cv-fold-{}".format(i)
                    )
            else:  # train case
                _log_importance(env.model, max_num_features)

    return callback
