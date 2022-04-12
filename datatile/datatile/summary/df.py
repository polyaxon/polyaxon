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

import numpy as np
import pandas as pd

from traceml.processors import df_processors


class DataFrameSummary:
    ALL = "ALL"
    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"

    TYPE_BOOL = "bool"
    TYPE_NUMERIC = "numeric"
    TYPE_DATE = "date"
    TYPE_CATEGORICAL = "categorical"
    TYPE_CONSTANT = "constant"
    TYPE_UNIQUE = "unique"

    def __init__(self, df, plot=False):
        self.df = df
        self.length = len(df)
        self.columns_stats = df_processors.get_df_column_stats(self.df)
        self.corr = df.corr()
        self.plot = plot

    def __getitem__(self, column):
        if isinstance(column, str) and df_processors.df_has_column(
            df=self.df, column=column
        ):
            return df_processors.get_df_column_summary(
                df=self.df,
                column=column,
                columns_stats=self.columns_stats,
                df_length=self.length,
                plot=self.plot,
            )

        if isinstance(column, int) and column < self.df.shape[1]:
            return df_processors.get_df_column_summary(
                df=self.df,
                column=self.df.columns[column],
                columns_stats=self.columns_stats,
                df_length=self.length,
                plot=self.plot,
            )

        if isinstance(column, (tuple, list)):
            error_keys = [
                k
                for k in column
                if not df_processors.df_has_column(df=self.df, column=k)
            ]
            if len(error_keys) > 0:
                raise KeyError(", ".join(error_keys))
            return self.df[list(column)].values

        if isinstance(column, pd.Index):
            error_keys = [
                k
                for k in column.values
                if not df_processors.df_has_column(df=self.df, column=k)
            ]
            if len(error_keys) > 0:
                raise KeyError(", ".join(error_keys))
            return self.df[column].values

        if isinstance(column, np.ndarray):
            error_keys = [
                k
                for k in column
                if not df_processors.df_has_column(df=self.df, column=k)
            ]
            if len(error_keys) > 0:
                raise KeyError(", ".join(error_keys))
            return self.df[column].values

        raise KeyError(column)

    @property
    def columns_types(self):
        return df_processors.get_df_columns_types(self.columns_stats)

    def summary(self):
        return pd.concat([self.df.describe(), self.columns_stats], sort=True)[
            self.df.columns
        ]

    """ Column summaries """

    @property
    def constants(self):
        return self.df.columns[self.columns_stats.loc["types"] == "constant"]

    @property
    def categoricals(self):
        return self.df.columns[self.columns_stats.loc["types"] == "categorical"]

    @property
    def numerics(self):
        return self.df.columns[self.columns_stats.loc["types"] == "numeric"]

    @property
    def uniques(self):
        return self.df.columns[self.columns_stats.loc["types"] == "unique"]

    @property
    def bools(self):
        return self.df.columns[self.columns_stats.loc["types"] == "bool"]

    @property
    def missing_frac(self):
        return self.columns_stats.loc["missing"].apply(lambda x: float(x) / self.length)

    def get_columns(self, df, usage, columns=None):
        """
        Returns a `data_frame.columns`.
        :param df: dataframe to select columns from
        :param usage: should be a value from [ALL, INCLUDE, EXCLUDE].
                            this value only makes sense if attr `columns` is also set.
                            otherwise, should be used with default value ALL.
        :param columns: * if `usage` is all, this value is not used.
                        * if `usage` is INCLUDE, the `df` is restricted to the intersection
                          between `columns` and the `df.columns`
                        * if usage is EXCLUDE, returns the `df.columns` excluding these `columns`
        :return: `data_frame` columns, excluding `target_column` and `id_column` if given.
                 `data_frame` columns, including/excluding the `columns` depending on `usage`.
        """
        columns_excluded = pd.Index([])
        columns_included = df.columns

        if usage == self.INCLUDE:
            try:
                columns_included = columns_included.intersection(pd.Index(columns))
            except TypeError:
                pass
        elif usage == self.EXCLUDE:
            try:
                columns_excluded = columns_excluded.union(pd.Index(columns))
            except TypeError:
                pass

        columns_included = columns_included.difference(columns_excluded)
        return columns_included.intersection(df.columns)
