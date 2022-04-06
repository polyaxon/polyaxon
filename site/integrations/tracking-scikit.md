---
title: "Scikit Tracking"
meta_title: "Scikit Tracking"
meta_description: "Polyaxon allows to schedule Scikit-learn experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "The Scikit-learn is a free software machine learning library for the Python programming language. It features various classification, regression and clustering algorithms including support vector machines, ..."
image: "../../content/images/integrations/scikit.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
featured: false
popularity: 1
visibility: public
status: published
---

Polyaxon allows to schedule Scikit-learn experiments, and supports tracking metrics, outputs, and models.

With Polyaxon you can:

 * log hyperparameters for every run
 * see learning curves for metrics during training
 * see hardware consumption and stdout/stderr output during training
 * log images, charts, and other assets
 * log git commit information
 * log env information
 * log model
 * ...

## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with Scikit-learn.

## Setup

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Polyaxon callbacks

Polyaxon provides callbacks to report metrics automatically for classifiers and regressors:

```python
from polyaxon.tracking.contrib.scikit import log_classifier, log_regressor

# Regressor
log_regressor(regressor, X_test, y_test)

# Classier
log_classifier(classifier, X_test, y_test)
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom Scikit-learn scripts:

```python
from polyaxon import tracking

# Log your metrics
tracking.log_metrics(metric1=value1, metric2=value2, ...)
```

## Example

### Example classifier

In this example we will go through the process of logging a classifier information and logging a pickled model.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally.
 
To see how this can be turned to a declarative approach to be submitted to a Polyaxon cluster, please check this [example](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/sklearn/digits)

```python
import pickle
from sklearn.datasets import load_digits
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

from polyaxon.tracking.contrib.scikit import log_classifier
from polyaxon import tracking

parameters = {
    'n_estimators': 120,
    'learning_rate': 0.12,
    'min_samples_split': 3,
    'min_samples_leaf': 2,
}
gbc = GradientBoostingClassifier(**parameters)

X, y = load_digits()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=28743)

# Polyaxon
tracking.init(name="classifier", is_offline=True)
tracking.log_inputs(**parameters)
tracking.log_data_ref(content=X_train, name='x_train', is_input=True)
tracking.log_data_ref(content=y_train, name='y_train', is_input=True)
tracking.log_data_ref(content=X_test, name='x_test', is_input=True)
tracking.log_data_ref(content=y_test, name='y_test', is_input=True)

gbc.fit(X_train, y_train)

# Polyaxon
log_classifier(gbc, X_test, y_test)

# Logging the model as pickle
with tempfile.TemporaryDirectory() as d:
    model_path = os.path.join(d, "model.pkl")
    with open(model_path, "wb") as out:
        pickle.dump(gbc, out)
    tracking.log_model(model_path, name="model", framework="scikit-learn", versioned=False)

# End
tracking.end()
```

> **Note**: the `versioned` was removed in version `>v1.17` and is the default behavior.

### Example regressor

In this example we will go through the process of logging a regressor information and logging a joblib model.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally.
 
To see how this can be turned to a declarative approach to be submitted to a Polyaxon cluster, please check this [example](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/sklearn/boston)

```python
import os

import joblib
import tempfile
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from polyaxon.tracking.contrib.scikit import log_regressor
from polyaxon import tracking

parameters = {
    'n_estimators': 70,
    'max_depth': 7,
    'min_samples_split': 3,
}
rfr = RandomForestRegressor(**parameters)

X, y = load_boston(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=28743)

# Polyaxon
tracking.init(name="regressor")
tracking.log_inputs(**parameters)
tracking.log_data_ref(content=X_train, name='x_train', is_input=True)
tracking.log_data_ref(content=y_train, name='y_train', is_input=True)
tracking.log_data_ref(content=X_test, name='x_test', is_input=True)
tracking.log_data_ref(content=y_test, name='y_test', is_input=True)

rfr.fit(X_train, y_train)

# Polyaxon
log_regressor(rfr, X_test, y_test)

# Logging the model as joblib
with tempfile.TemporaryDirectory() as d:
    model_path = os.path.join(d, "model.joblib")
    joblib.dump(rfr, model_path)
    tracking.log_model(model_path, name="model", framework="scikit-learn", versioned=False)
```

> **Note**: the `versioned` was removed in version `>v1.17` and is the default behavior.
