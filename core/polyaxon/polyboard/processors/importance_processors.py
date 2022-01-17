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
import math
import numpy as np
import pandas as pd

from typing import Dict, List, Optional, Tuple, Union

from polyaxon.utils.np_utils import sanitize_np_types


def clean_duplicates(
    metrics: pd.DataFrame, configs: pd.DataFrame
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    duplicate_ids = metrics.duplicated()
    configs_df = configs[~duplicate_ids]
    metrics_df = metrics[~duplicate_ids]
    if configs.empty or metrics.empty:
        return None

    configs_df = pd.get_dummies(configs_df)
    configs_df = configs_df.loc[:, ~configs_df.columns.duplicated()]
    return metrics_df, configs_df


def clean_values(
    metrics: List[Union[int, float]], configs: List[Dict]
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    if not metrics or not configs:
        return None

    for m in metrics:
        if not isinstance(m, (int, float)):
            return None

    metrics_df = pd.DataFrame(metrics)
    if metrics_df.isnull().values.any():
        return None

    configs_df = pd.DataFrame.from_records(configs).replace(
        r"^\s*$", np.nan, regex=True
    )
    for col in configs_df.columns:
        if not configs_df[col].isnull().sum() == len(configs_df[col]):
            if configs_df[col].dtype == "object":
                configs_df[col].fillna("NAN", inplace=True)
                configs_df[col].fillna("NAN", inplace=True)
                configs_df[col] = configs_df[col].astype("category")
            elif configs_df[col].dtype == "float64" or configs_df[col].dtype == "int64":
                configs_df[col].fillna(configs_df[col].mean(), inplace=True)
            else:
                print("Unexpected Column type: {}".format(configs_df[col].dtype))
        else:
            if configs_df[col].dtype == "object":
                configs_df[col] = "NAN"
            elif configs_df[col].dtype == "float64" or configs_df[col].dtype == "int64":
                configs_df[col] = 0

    return clean_duplicates(metrics_df, configs_df)


def _get_value(x):
    if x is None or math.isnan(x):
        return None
    return round(sanitize_np_types(x), 3)


def calculate_importance(metrics: List[Union[int, float]], configs: List[Dict]):
    values = clean_values(metrics, configs)
    if not values:
        return None
    metrics_df, configs_df = values

    corr_list = configs_df.corrwith(metrics_df[0])

    from sklearn.ensemble import ExtraTreesRegressor

    forest = ExtraTreesRegressor(n_estimators=250, random_state=0)
    forest.fit(configs_df, metrics_df[0])
    feature_importances = forest.feature_importances_

    results = {}
    for i, name in enumerate(configs_df.columns):
        results[name] = {
            "importance": _get_value(feature_importances[i]),
            "correlation": _get_value(corr_list[name]),
        }
    return results
