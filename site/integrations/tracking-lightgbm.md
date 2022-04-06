---
title: "LightGBM Tracking"
meta_title: "LightGBM Tracking"
meta_description: "Polyaxon allows to schedule LightGBM experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "LightGBM, short for Light Gradient Boosting Machine, is a free and open source distributed gradient boosting framework for machine learning originally developed by Microsoft. It is based on decision tree algorithms and used for ranking, classification and other machine learning tasks."
image: "../../content/images/integrations/lightgbm.png"
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

Polyaxon allows to schedule LightGBM experiments and supports tracking metrics, outputs, and models.

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

You can use the tracking API to create a custom tracking experience with LightGBM.

## Setup

In order to use Polyaxon tracking with LightGBM, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Polyaxon callback

Pass Polyaxon's callback to the `train` function

```python
from polyaxon.tracking.contrib.lightgbm import polyaxon_callback

gbm = lgb.train(
    params,
    lgb_train,
    num_boost_round=500,
    valid_sets=[lgb_train, lgb_eval],
    valid_names=['train','valid'],
    callbacks=[polyaxon_callback()],
)
```

## Customizing the callback

Creating the callback will use the current initialized run, but you can use a different run if you need to have more control:

```python
from polyaxon.tracking import Run
from polyaxon.tracking.contrib.lightgbm import polyaxon_callback

run = Run(...)

gbm = lgb.train(
    ...,
    callbacks = [polyaxon_callback(run)],
)
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your scripts, you just need to add `tracking.log_...` anywhere needed:

 * log metrics

```python
tracking.log_mtrics(loss=loss)
```

 * log artifacts
 
```python
tracking.log_artifact_ref(asset_path)
```

## Example

In this example we will go through the process of logging a LightGBM model using Polyaxon's callback.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally. 

To see how this can be turned to a declarative approach to be submitted to a Polyaxon cluster, please check this [example](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/lightgbm/wine)

```python
import argparse
import logging

import lightgbm as lgb

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.lightgbm import polyaxon_callback

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--boosting_type',
        type=str,
        default='gbdt'
    )
    parser.add_argument(
        '--objective',
        type=str,
        default='multiclass'
    )
    parser.add_argument(
        '--num_class',
        type=int,
        default=3
    )
    parser.add_argument(
        '--num_leaves',
        type=int,
        default=31
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.05,
    )
    parser.add_argument(
        '--feature_fraction',
        type=float,
        default=0.9
    )

    args = parser.parse_args()

    params = {
        'boosting_type': args.boosting_type,
        'objective': args.objective,
        'num_class': args.num_class,
        'num_leaves': args.num_leaves,
        'learning_rate': args.learning_rate,
        'feature_fraction': args.feature_fraction,
    }

    # Polyaxon
    tracking.init(is_offline=True)

    data = load_wine()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.1)

    # Polyaxon
    tracking.log_data_ref(content=X_train, name='x_train', is_input=True)
    tracking.log_data_ref(content=y_train, name='y_train', is_input=True)
    tracking.log_data_ref(content=X_test, name='X_test', is_input=True)
    tracking.log_data_ref(content=y_test, name='y_train', is_input=True)

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    gbm = lgb.train(
        params,
        lgb_train,
        num_boost_round=500,
        valid_sets=[lgb_train, lgb_eval],
        valid_names=['train', 'valid'],
        callbacks=[polyaxon_callback()],  # Polyaxon
    )

    y_test_pred = gbm.predict(X_test)

    # Polyaxon
    tracking.log_sklearn_roc_auc_curve("roc_c", y_test_pred, y_test, is_multi_class=True)

    model_path = tracking.get_outputs_path("model/lightgbm.pkl")
    gbm.save_model(model_path)

    # Polyaxon
    tracking.log_model_ref(model_path, framework="lightgbm")
```

