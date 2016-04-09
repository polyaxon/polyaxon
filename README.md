# pandas_summary
An extension to [pandas](http://pandas.pydata.org/) dataframes describe function.

The module contains `DataFrameSummary` object that extend `describe()` with:

 * **properties**
    * dfs.columns_stats: counts, uniques, missing, missing_perc, and type per column
    * dsf.columns_types: a count of the types of columns
    * dfs[column]: more in depth summary of the column
 * **function**
    * summary(): extends the `describe()` function with the values with `columns_stats`
 

# Installation
The module can be easily installed with pip:

```conslole
> pip install pandas-summary
```

This module depends on `numpy` and `pandas`. Optionally you can get also some nice visualisations if you have `matplotlib` installed.

# Tests
To run the tests, execute the command `python setup.py test`

# Usage
The module contains one class:

## DataFrameSummary

The `DataFrameSummary` expect a pandas `DataFrame` to summarise.

```python
from pandas_summary import DataFrameSummary

dfs = DataFrameSummary(df)
```

getting the columns types

```python
dfs.columns_types


numeric     9
bool        3
categorical 2
unique      1
date        1
constant    1
dtype: int64
```

getting the columns stats

```python
dfs.columns_stats


                      A            B        C              D              E 
counts             5802         5794     5781           5781           4617   
uniques            5802            3     5771            128            121   
missing               0            8       21             21           1185   
missing_perc         0%        0.14%    0.36%          0.36%         20.42%   
types            unique  categorical  numeric        numeric        numeric 
```

getting a single column summary, e.g. numerical column

```python
# we can also access the column using numbers A[1]
dfs['A']

std                                                                 0.2827146
max                                                                  1.072792
min                                                                         0
variance                                                           0.07992753
mean                                                                0.5548516
5%                                                                  0.1603367
25%                                                                 0.3199776
50%                                                                 0.4968588
75%                                                                 0.8274732
95%                                                                  1.011255
iqr                                                                 0.5074956
kurtosis                                                            -1.208469
skewness                                                            0.2679559
sum                                                                  3207.597
mad                                                                 0.2459508
cv                                                                  0.5095319
zeros_num                                                                  11
zeros_perc                                                               0,1%
deviating_of_mean                                                          21
deviating_of_mean_perc                                                  0.36%
deviating_of_median                                                        21
deviating_of_median_perc                                                0.36%
top_correlations                         {u'D': 0.702240243124, u'E': -0.663}
counts                                                                   5781
uniques                                                                  5771
missing                                                                    21
missing_perc                                                            0.36%
types                                                                 numeric
Name: A, dtype: object
```

# Future development

Summary analysis between columns, i.e. `dfs[[1, 2]]`
