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
import math
import numpy as np
import pandas as pd

from typing import Dict, List, Optional, Tuple, Union

from polyaxon.utils.np_utils import sanitize_np_types


def clean_duplicates(
    params: pd.DataFrame, metrics: pd.DataFrame
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    duplicate_ids = metrics.duplicated()
    params_df = params[~duplicate_ids]
    metrics_df = metrics[~duplicate_ids]
    if params.empty or metrics.empty:
        return None

    params_df = pd.get_dummies(params_df)
    params_df = params_df.loc[:, ~params_df.columns.duplicated()]
    return params_df, metrics_df


def clean_values(
    params: List[Dict], metrics: List[Union[int, float]]
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    if not metrics or not params:
        return None

    for m in metrics:
        if not isinstance(m, (int, float)):
            return None

    metrics_df = pd.DataFrame(metrics)
    if metrics_df.isnull().values.any():
        return None

    params_df = pd.DataFrame.from_records(params).replace(r"^\s*$", np.nan, regex=True)
    for col in params_df.columns:
        if not params_df[col].isnull().sum() == len(params_df[col]):
            if params_df[col].dtype == "object":
                params_df[col].fillna("NAN", inplace=True)
                params_df[col].fillna("NAN", inplace=True)
                params_df[col] = params_df[col].astype("category")
            elif params_df[col].dtype == "float64" or params_df[col].dtype == "int64":
                params_df[col].fillna(params_df[col].mean(), inplace=True)
            else:
                print("Unexpected Column type: {}".format(params_df[col].dtype))
        else:
            if params_df[col].dtype == "object":
                params_df[col] = "NAN"
            elif params_df[col].dtype == "float64" or params_df[col].dtype == "int64":
                params_df[col] = 0

    return clean_duplicates(params_df, metrics_df)


def _get_value(x):
    if x is None or math.isnan(x):
        return None
    return round(sanitize_np_types(x), 3)


def calculate_importance_correlation(
    params: List[Dict], metrics: List[Union[int, float]]
):
    values = clean_values(params, metrics)
    if not values:
        return None
    params_df, metrics_df = values

    corr_list = params_df.corrwith(metrics_df[0])

    from sklearn.ensemble import ExtraTreesRegressor

    forest = ExtraTreesRegressor(n_estimators=250, random_state=0)
    forest.fit(params_df, metrics_df[0])
    feature_importances = forest.feature_importances_

    results = {}
    for i, name in enumerate(params_df.columns):
        results[name] = {
            "importance": _get_value(feature_importances[i]),
            "correlation": _get_value(corr_list[name]),
        }
    return results
