---
title: "XGBoost Tracking"
meta_title: "XGBoost Tracking"
meta_description: "Polyaxon allows to schedule XGBoost experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "XGBoost is an open-source software library which provides a gradient boosting framework for C++, Java, Python, R, Julia, Perl, and Scala. It works on Linux, Windows, and macOS. From the project description, it aims to provide a 'Scalable, Portable and Distributed Gradient Boosting Library'."
image: "../../content/images/integrations/xgboost.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
featured: false
popularity: 2
visibility: public
status: published
---

Polyaxon allows to schedule XGBoost experiments and supports tracking metrics, outputs, and models.

With Polyaxon you can:

 * log hyperparameters for every run
 * see learning curves for losses and metrics during training
 * see hardware consumption and stdout/stderr output during training
 * log images, charts, and other assets
 * log git commit information
 * log env information
 * log model
 * ...

## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with XGBoost.

## Setup

In order to use Polyaxon tracking with XGBoost, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## XGBoost callback

Polyaxon provides two XGBoost callback flavors an old `polyaxon_callback` function and a new `PolyaxonCallback` class, you can use one of these callbacks with your experiment to report metrics automatically and other charts automatically:

 * Function callback

```python
from polyaxon import tracking
from polyaxon.tracking.contrib.xgboost import polyaxon_callback

# ...
tracking.init()
#...
model.train(params, data, callbacks=[polyaxon_callback(...)])
```

 * Class callback

> **Note**: this callback is available from `>1.17.0`

```python
from polyaxon import tracking
from polyaxon.tracking.contrib.xgboost import PolyaxonCallback

# ...
tracking.init()
#...
model.train(params, data, callbacks=[PolyaxonCallback(...)])
```

## Customizing the callback

Creating the callback will use the current initialized run, but you can use a different run if you need to have more control:

 * Function callback

```python
from polyaxon.tracking import Run
from polyaxon.tracking.contrib.xgboost import polyaxon_callback

run = Run(...)

model.train(params, data, callbacks=[polyaxon_callback(run=run, log_importance=True, log_model=True, max_num_features=44)])
```


 * Class callback

```python
from polyaxon.tracking import Run
from polyaxon.tracking.contrib.xgboost import polyaxon_callback

run = Run(...)

model.train(params, data, callbacks=[polyaxon_callback(run=run, log_importance=True, log_model=True, max_num_features=44)])
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom XGBoost scripts:

 * log metrics

```python
tracking.log_mtrics(metric1=value1, metric2=value2, ...)
```

## Example

In this example we will go through the process of logging an XGBoost model using Polyaxon's callback.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally. 

To see how this can be turned to a declarative approach to be submitted to a Polyaxon cluster, please check this [example](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/sklearn/boston)


```python
import argparse
import logging

import pandas as pd
import xgboost as xgb

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.xgboost import polyaxon_callback, PolyaxonCallback

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--max_depth',
        type=int,
        default=5
    )
    parser.add_argument(
        '--eta',
        type=int,
        default=0.5
    )
    parser.add_argument(
        '--gamma',
        type=int,
        default=0.1
    )
    parser.add_argument(
        '--subsample',
        type=int,
        default=1
    )
    parser.add_argument(
        '--lambda',
        type=int,
        default=1,
        dest='lambda_',
    )
    parser.add_argument(
        '--alpha',
        type=float,
        default=0.35
    )
    parser.add_argument(
        '--objective',
        type=str,
        default='reg:squarederror'
    )
    parser.add_argument(
        '--cross_validate',
        type=bool,
        default=False
    )

    args = parser.parse_args()

    params = {
        'max_depth': args.max_depth,
        'eta': args.eta,
        'gamma': args.gamma,
        'subsample': args.subsample,
        'lambda': args.lambda_,
        'alpha': args.alpha,
        'objective': args.objective,
        'eval_metric': ['mae', 'rmse']
    }

    # Polyaxon
    tracking.init()

    boston = load_boston()
    data = pd.DataFrame(boston.data)
    data.columns = boston.feature_names
    data['PRICE'] = boston.target
    X, y = data.iloc[:, :-1], data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1012)

    # Polyaxon
    tracking.log_data_ref(content=X_train, name='x_train', is_input=True)
    tracking.log_data_ref(content=y_train, name='y_train', is_input=True)
    tracking.log_data_ref(content=X_test, name='X_test', is_input=True)
    tracking.log_data_ref(content=y_test, name='y_train', is_input=True)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    
    callback = polyaxon_callback()
    # Or 
    # callback = PolyaxonCallback()

    if args.cross_validate:
        xgb.cv(params, dtrain, num_boost_round=20, nfold=7,
               callbacks=[callback])
    else:
        xgb.train(params, dtrain, 20, [(dtest, 'eval'), (dtrain, 'train')],
                  callbacks=[callback])
```
