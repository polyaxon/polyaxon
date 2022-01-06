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

from typing import List, Union

from polyaxon_schemas.constants import INCLUDE, EXCLUDE, ALL
from polyaxon_schemas.utils.units import to_percentage

try:
    import pandas as pd
    from pandas.api import pd_types
except ImportError:
    pd = None

NUMPY_ERROR_MESSAGE = "numpy is required for this tracking operation!"
PANDAS_ERROR_MESSAGE = "pandas is required for this tracking operation!"

DF_TYPE_BOOL = 'bool'
DF_TYPE_NUMERIC = 'numeric'
DF_TYPE_DATE = 'date'
DF_TYPE_CATEGORICAL = 'categorical'
DF_TYPE_CONSTANT = 'constant'
DF_TYPE_UNIQUE = 'unique'


def get_df_columns(df: pd.DataFrame, usage: Union[INCLUDE, EXCLUDE, ALL], columns: Union[pd.Index, List[str]] = None):
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



def get_df_columns_stats(df: pd.DataFrame, df_length: int = None, df_counts: int = None, df_uniques: pd.Series = None):
    if df_counts is None:
        df_counts = df.count()
        df_counts.name = 'counts'
    if df_uniques is None:
        df_uniques = get_df_uniques(df=df)
    missing = get_df_missing(df=df, df_length=df_length, df_counts=df_counts)
    stats = pd.concat([df_counts, df_uniques, missing], axis=1, sort=True)

    # settings types
    stats['types'] = ''
    columns_info = get_df_columns_info(stats)
    for ctype, columns in columns_info.items():
        stats.loc[columns, 'types'] = ctype
    return stats.transpose()[df.columns]


def columns_types(df: pd.DataFrame, columns_stats = None, df_length: int = None, df_counts: int = None, df_uniques: pd.Series = None):
    if columns_stats is None:
        columns_stats = get_df_columns_stats(df=df, df_length=df_length, df_counts=df_counts, df_uniques=df_uniques)
    return pd.value_counts(columns_stats.loc['types'])


def get_df_uniques(df: pd.DataFrame):
    return pd.Series(dict((c, df[c].nunique()) for c in df.columns), name='uniques')


def get_df_missing(df: pd.DataFrame, df_length: int = None, df_counts: int = None):
    if df_length is None:
        df_length = len(df)
    if df_counts is None:
        df_counts = df.count()
        df_counts.name = 'counts'
    count = df_length - df_counts
    count.name = 'missing'
    perc = (count / df_length).apply(to_percentage)
    perc.name = 'missing_perc'
    return pd.concat([count, perc], axis=1, sort=True)


def get_df_stats(df: pd.DataFrame, df_counts: int = None) -> pd.DataFrame:
    def get_df_columns_info():
        column_info = {}
        column_info[DF_TYPE_CONSTANT] = stats['uniques'][stats['uniques'] == 1].index
        column_info[DF_TYPE_BOOL] = stats['uniques'][stats['uniques'] == 2].index
        rest_columns = get_df_columns(df, EXCLUDE,
                                      column_info['constant'].union(column_info['bool']))
        column_info[DF_TYPE_NUMERIC] = pd.Index([c for c in rest_columns
                                                 if pd_types.is_numeric_dtype(df[c])])
        rest_columns = get_df_columns(df[rest_columns], EXCLUDE, column_info['numeric'])
        column_info[DF_TYPE_DATE] = pd.Index([c for c in rest_columns
                                              if pd_types.is_datetime64_dtype(df[c])])
        rest_columns = get_df_columns(df[rest_columns], EXCLUDE, column_info['date'])
        unique_columns = stats['uniques'][rest_columns] == stats['counts'][rest_columns]
        column_info[DF_TYPE_UNIQUE] = stats['uniques'][rest_columns][unique_columns].index
        column_info[DF_TYPE_CATEGORICAL] = stats['uniques'][rest_columns][~unique_columns].index
        return column_info

    if df_counts is None:
        df_counts = df.count()
        df_counts.name = 'counts'
    uniques = get_df_uniques(df)
    missing = get_df_missing(df=df, df_counts=df_counts)
    stats = pd.concat([df_counts, uniques, missing], axis=1, sort=True)

    # settings types
    stats['types'] = ''
    columns_info = get_df_columns_info()
    for ctype, columns in columns_info.items():
        stats.loc[columns, 'types'] = ctype
    return stats.transpose()[df.columns]


def get_df_columns_types(columns_stats: pd.DataFrame):
    return pd.value_counts(columns_stats.loc['types'])
