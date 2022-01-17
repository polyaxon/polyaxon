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

from typing import Dict, List, Tuple, Union

from polyaxon.utils.units import to_percentage

NUMPY_ERROR_MESSAGE = "numpy is required for this tracking operation!"
PANDAS_ERROR_MESSAGE = "pandas is required for this tracking operation!"

try:
    import numpy as np
except ImportError as e:
    raise ImportError(NUMPY_ERROR_MESSAGE) from e

try:
    import pandas as pd

    from pandas.api import types as pd_types
except ImportError:
    raise ImportError(PANDAS_ERROR_MESSAGE) from e

DF_TYPE_BOOL = "bool"
DF_TYPE_NUMERIC = "numeric"
DF_TYPE_DATE = "date"
DF_TYPE_CATEGORICAL = "categorical"
DF_TYPE_CONSTANT = "constant"
DF_TYPE_UNIQUE = "unique"

EXCLUDE = "exclude"
INCLUDE = "include"
RAISE = "raise"
ALL = "all"


def df_has_column(df: pd.DataFrame, column: Union[int, str]):
    if not isinstance(column, (int, str)):
        raise ValueError("{} is not a valid column".format(column))
    return column in df.columns


def get_df_columns(
    df: pd.DataFrame,
    usage: Union[INCLUDE, EXCLUDE, ALL],
    columns: Union[pd.Index, List[str]] = None,
):
    """
    Returns a `pd.DataFrame.columns`.

    Args:
        df: dataframe to select columns from
        usage: should be a value from [ALL, INCLUDE, EXCLUDE].
             this value only makes sense if attr `columns` is also set.
             otherwise, should be used with default value ALL.
        columns:
             * if `usage` is all, this value is not used.
             * if `usage` is INCLUDE, the `df` is restricted to the intersection
             between `columns` and the `df.columns`
             * if usage is EXCLUDE, returns the `df.columns` excluding these `columns`
    Returns:
        `pd.DataFrame` columns, excluding `target_column` and `id_column` if given.
        `pd.DataFrame` columns, including/excluding the `columns` depending on `usage`.
    """
    columns_excluded = pd.Index([])
    columns_included = df.columns

    if usage == INCLUDE:
        try:
            columns_included = columns_included.intersection(pd.Index(columns))
        except TypeError:
            pass
    elif usage == EXCLUDE:
        try:
            columns_excluded = columns_excluded.union(pd.Index(columns))
        except TypeError:
            pass

    columns_included = columns_included.difference(columns_excluded)
    return columns_included.intersection(df.columns)


def get_df_uniques(df: pd.DataFrame):
    return pd.Series(dict((c, df[c].nunique()) for c in df.columns), name="uniques")


def get_df_missing(df: pd.DataFrame, df_length: int = None, df_counts: int = None):
    if df_length is None:
        df_length = len(df)
    if df_counts is None:
        df_counts = df.count()
        df_counts.name = "counts"
    count = df_length - df_counts
    count.name = "missing"
    perc = (count / df_length).apply(to_percentage)
    perc.name = "missing_perc"
    return pd.concat([count, perc], axis=1, sort=True)


def get_df_column_stats(df: pd.DataFrame, df_counts: int = None) -> pd.DataFrame:
    def get_df_columns_info():
        column_info = {}
        column_info[DF_TYPE_CONSTANT] = stats["uniques"][stats["uniques"] == 1].index
        column_info[DF_TYPE_BOOL] = stats["uniques"][stats["uniques"] == 2].index
        rest_columns = get_df_columns(
            df, EXCLUDE, column_info["constant"].union(column_info["bool"])
        )
        column_info[DF_TYPE_NUMERIC] = pd.Index(
            [c for c in rest_columns if pd_types.is_numeric_dtype(df[c])]
        )
        rest_columns = get_df_columns(df[rest_columns], EXCLUDE, column_info["numeric"])
        column_info[DF_TYPE_DATE] = pd.Index(
            [c for c in rest_columns if pd_types.is_datetime64_dtype(df[c])]
        )
        rest_columns = get_df_columns(df[rest_columns], EXCLUDE, column_info["date"])
        unique_columns = stats["uniques"][rest_columns] == stats["counts"][rest_columns]
        column_info[DF_TYPE_UNIQUE] = stats["uniques"][rest_columns][
            unique_columns
        ].index
        column_info[DF_TYPE_CATEGORICAL] = stats["uniques"][rest_columns][
            ~unique_columns
        ].index
        return column_info

    if df_counts is None:
        df_counts = df.count()
        df_counts.name = "counts"
    uniques = get_df_uniques(df)
    missing = get_df_missing(df=df, df_counts=df_counts)
    stats = pd.concat([df_counts, uniques, missing], axis=1, sort=True)

    # settings types
    stats["types"] = ""
    columns_info = get_df_columns_info()
    for ctype, columns in columns_info.items():
        stats.loc[columns, "types"] = ctype
    return stats.transpose()[df.columns]


def get_df_columns_types(columns_stats: pd.DataFrame):
    return pd.value_counts(columns_stats.loc["types"])


def get_deviation_of_mean(
    series: pd.Series, multiplier: int = 3, df_length: int = None
) -> Tuple[int, float]:
    """
    Returns count of values deviating of the mean, i.e. larger than `multiplier` * `std`.
    Args:
        series: Series to perform operation over.
        multiplier: The value to use as
    Returns:
        tuple
    """
    if df_length is None:
        df_length = len(series)
    capped_series = np.minimum(series, series.mean() + multiplier * series.std())
    count = pd.value_counts(series != capped_series)
    count = count[True] if True in count else 0
    return count, to_percentage(count / df_length)


def get_median_absolute_deviation(
    series, multiplier=3, df_length: int = None
) -> Tuple[int, float]:
    """
    Returns count of values larger than `multiplier` * `mad`
    Args:
        series: Series to perform operation over.
        multiplier: The value to use as
    Returns:
        tuple
    """
    if df_length is None:
        df_length = len(series)
    capped_series = np.minimum(series, series.median() + multiplier * series.mad())
    count = pd.value_counts(series != capped_series)
    count = count[True] if True in count else 0
    return count, to_percentage(count / df_length)


def get_top_correlations(
    df: pd.DataFrame, column: str, threshold: float = 0.65, top: int = 3, df_corr=None
) -> Dict:
    """
    Returns count of values larger than `multiplier` * `mad`
    Args:
        df: dataframe.
        column: name of the column to calculate correlation for.
    Returns:
        tuple
    """
    if df_corr is None:
        df_corr = df.corr()
    column_corr = np.fabs(df_corr[column].drop(column)).sort_values(
        ascending=False, inplace=False
    )
    top_corr = column_corr[(column_corr > threshold)][:top].index
    return df_corr[column][top_corr].to_dict()


def get_top_correlations_description(
    df: pd.DataFrame, column: str, threshold: float = 0.65, top: int = 3, df_corr=None
) -> str:
    correlations = get_top_correlations(
        df=df, column=column, threshold=threshold, top=top, df_corr=df_corr
    )
    return ", ".join(
        "{}: {}".format(col, to_percentage(val)) for col, val in correlations.items()
    )


def get_numeric_summary(
    df: pd.DataFrame,
    column: str,
    columns_stats: pd.DataFrame = None,
    df_length: int = None,
    plot: bool = False,
):
    series = df[column]

    if plot:
        try:
            series.hist()
        except ImportError:
            pass

    if df_length is None:
        df_length = len(series)

    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    stats = {
        "mean": series.mean(),
        "std": series.std(),
        "variance": series.var(),
        "min": series.min(),
        "max": series.max(),
        "mode": series.mode()[0],
    }

    for x in np.array([0.05, 0.25, 0.5, 0.75, 0.95]):
        stats[to_percentage(x)] = series.quantile(x)

    stats["iqr"] = stats["75%"] - stats["25%"]
    stats["kurtosis"] = series.kurt()
    stats["skewness"] = series.skew()
    stats["sum"] = series.sum()
    stats["mad"] = series.mad()
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.nan
    stats["zeros_num"] = df_length - np.count_nonzero(series)
    stats["zeros_perc"] = to_percentage(stats["zeros_num"] / df_length)
    deviation_of_mean, deviation_of_mean_perc = get_deviation_of_mean(
        series, df_length=df_length
    )
    stats["deviating_of_mean"] = deviation_of_mean
    stats["deviating_of_mean_perc"] = deviation_of_mean_perc
    (
        deviating_of_median,
        deviating_of_median_perc,
    ) = get_median_absolute_deviation(series, df_length=df_length)
    stats["deviating_of_median"] = deviating_of_median
    stats["deviating_of_median_perc"] = deviating_of_median_perc
    stats["top_correlations"] = get_top_correlations_description(df=df, column=column)
    return pd.concat([pd.Series(stats, name=column), columns_stats[column]], sort=True)


def get_date_summary(df: pd.DataFrame, column: str, columns_stats: pd.DataFrame = None):
    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    series = df[column]
    stats = {"min": series.min(), "max": series.max()}
    stats["range"] = stats["max"] - stats["min"]
    return pd.concat([pd.Series(stats, name=column), columns_stats[column]], sort=True)


def get_categorical_summary(
    df: pd.DataFrame, column: str, columns_stats: pd.DataFrame = None
):
    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    series = df[column]
    # Only run if at least 1 non-missing value
    value_counts = series.value_counts()
    stats = {
        "top": "{}: {}".format(value_counts.index[0], value_counts.iloc[0]),
    }
    return pd.concat([pd.Series(stats, name=column), columns_stats[column]], sort=True)


def get_constant_summary(df: pd.DataFrame, column: str):
    return "This is a constant value: {}".format(df[column][0])


def get_bool_summary(
    df: pd.DataFrame,
    column: str,
    columns_stats: pd.DataFrame = None,
    df_length: int = None,
):
    series = df[column]

    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    if df_length is None:
        df_length = len(series)

    stats = {}
    for class_name, class_value in sorted(dict(series.value_counts()).items()):
        stats['"{}" count'.format(class_name)] = "{}".format(class_value)
        stats['"{}" perc'.format(class_name)] = "{}".format(
            to_percentage(class_value / df_length)
        )

    return pd.concat([pd.Series(stats, name=column), columns_stats[column]], sort=True)


def get_unique_summary(
    df: pd.DataFrame, column: str, columns_stats: pd.DataFrame = None
):
    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    return columns_stats[column]


def get_df_column_summary(
    df: pd.DataFrame,
    column: str,
    columns_stats: pd.DataFrame = None,
    df_length: int = None,
    plot: bool = False,
):
    if columns_stats is None:
        columns_stats = get_df_column_stats(df)

    if df_length is None:
        df_length = len(df)

    column_type = columns_stats.loc["types"][column]
    if column_type == DF_TYPE_NUMERIC:
        return get_numeric_summary(
            df=df,
            column=column,
            columns_stats=columns_stats,
            df_length=df_length,
            plot=plot,
        )
    if column_type == DF_TYPE_CATEGORICAL:
        return get_categorical_summary(
            df=df, column=column, columns_stats=columns_stats
        )
    if column_type == DF_TYPE_BOOL:
        return get_bool_summary(
            df=df, column=column, columns_stats=columns_stats, df_length=df_length
        )
    if column_type == DF_TYPE_UNIQUE:
        return get_unique_summary(df=df, column=column, columns_stats=columns_stats)
    if column_type == DF_TYPE_DATE:
        return get_date_summary(df=df, column=column, columns_stats=columns_stats)
    if column_type == DF_TYPE_CONSTANT:
        return get_constant_summary(df=df, column=column)
